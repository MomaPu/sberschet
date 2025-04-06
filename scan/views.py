from django.views.decorators import gzip
from django.http import StreamingHttpResponse, HttpResponse, JsonResponse
import cv2
import threading
import base64

class VideoCamera(object):
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.video = cv2.VideoCapture(camera_index)
        print(f"Камера {camera_index} открыта: {self.video.isOpened()}")

        if not self.video.isOpened():
            raise Exception(f"Не удалось открыть камеру с индексом {camera_index}")

        self.grabbed, self.frame = self.video.read()
        print(f"Первый кадр захвачен: {self.grabbed}")
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()
        print(f"Камера {self.camera_index} закрыта")

    def get_frame(self):
        if not self.grabbed:
            print("Кадр не захвачен. Возвращаем None.")
            return None

        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            grabbed, frame = self.video.read()

            if grabbed:
                self.grabbed = grabbed
                self.frame = frame
            else:
                print("Не удалось захватить кадр в потоке update")
                break #Выходим из цикла если не удалось захватить кадр


# Глобальная переменная для хранения объекта VideoCamera
camera = None

@gzip.gzip_page
def livefe(request):
    global camera
    if camera is None:
       return HttpResponse("Камера еще не запущена", status=503)

    try:
        return StreamingHttpResponse(gen(camera), content_type="multipart/x-mixed-replace;boundary=frame")
    except Exception as e:
        print(f"Ошибка в livefe: {e}")
        return HttpResponse("Ошибка при получении видеопотока", status=500)


def gen(camera):
    while True:
        if camera is not None:
            frame = camera.get_frame()
            if frame is not None:
                yield(b'--frame\r\n'
                      b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            else:
                print("Не удалось получить кадр в gen")
                break
        else:
            print("Камера не инициализирована в gen")
            break #Прерываем цикл

def capture_photo(request):
    global camera

    if camera is None:
        return HttpResponse("Камера еще не запущена", status=503)
    try:
        frame = camera.get_frame()
        # Преобразовать в base64 для отображения в HTML
        _, encoded_img = cv2.imencode('.jpg', camera.frame) #Использовать frame
        frame_data = base64.b64encode(encoded_img.tobytes()).decode('utf-8')
        return HttpResponse(f'<img src="" alt="Captured Photo">')

    except Exception as e:
        print(f"Ошибка при захвате фото: {e}")
        return HttpResponse("Ошибка при захвате фото", status=500)

def find_camera_index(request):
     for i in range(10):  # Проверяем первые 10 камер
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cap.release()
            return JsonResponse({'camera_index': i})

     return JsonResponse({'error': 'Камера не найдена'}, status=404)

def start_camera(request):

    global camera
    camera_index = request.GET.get('camera_index') #Получаем индекс

    if camera_index is None:
        return JsonResponse({'error': 'Не указан camera_index'}, status=400)
    try:
        camera_index = int(camera_index)
        camera = VideoCamera(camera_index=camera_index)
        return HttpResponse(status=200)
    except Exception as e:
        print(f"Ошибка при инициализации камеры: {e}")
        return JsonResponse({'error': f"Ошибка при запуске камеры: {e}"}, status=500)