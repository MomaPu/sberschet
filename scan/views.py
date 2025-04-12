from django.http import HttpResponse
from django.shortcuts import render
from .forms import HotelForm
from PIL import Image
import io
import base64
# Pillow library

def hotel_image_view(request):
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['hotel_Main_Img']  # Access the image file
            img = Image.open(image_file)  # Open with Pillow
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            img_str = base64.b64encode(buffer.getvalue()).decode()

            return render(request, 'scaner.html', {'form': form, 'uploaded_image_base64': img_str})

    else:
        form = HotelForm()
    return render(request, 'scaner.html', {'form': form})


def success(request):
    return HttpResponse('successfully uploaded')