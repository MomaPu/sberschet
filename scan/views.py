from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Hotel, User
from .forms import HotelForm, HomepageForm, ProfileForm
from PIL import Image
import io
import base64
#from apple_ocr.ocr import OCR

def hotel_image_view(request):
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
            hotel_instance = form.save(commit=False)

            # Сохраняем изображение
            image_file = request.FILES['hotel_Main_Img']
            img = Image.open(image_file)

            # Можно сохранить сразу файл или обработать
            # Для сохранения в модель
            hotel_instance.hotel_Main_Img = image_file
            hotel_instance.save()

            return redirect('../success')  # замените на ваш URL
    else:
        form = HotelForm()
    return render(request, 'scaner.html', {'form': form})


def success(request):
    return HttpResponse('successfully uploaded')

def homepage(request):
    form = HomepageForm(request.POST, request.FILES)
    return render(request, 'homepage.html', {'form': form})


def profile(request):
    form = ProfileForm(request.POST, request.FILES)
    return render(request, 'profile.html', {'form': form})