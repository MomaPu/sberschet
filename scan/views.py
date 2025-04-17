from django.http import HttpResponse
from .models import Hotel, User
from .forms import HotelForm, HomepageForm, ProfileForm
from PIL import Image
import io
import base64
from apple_ocr.ocr import OCR
from django.shortcuts import render, redirect
from django.urls import reverse

KEYWORDS = ['сумма', 'итог', 'загальна', 'всего', 'total', 'sum', 'amount', 'due', 'balance', 'итого к оплате:', 'к оплате']

def hotel_image_view(request):
    context = {}
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
            hotel_instance = form.save(commit=False)
            
            image_file = request.FILES['hotel_Main_Img']
            img = Image.open(image_file)
            
            ocr_instance = OCR(image=img)
            data = ocr_instance.recognize()
            
            for parts in data['Content']:
                if str(parts).lower() in KEYWORDS:
                    index = list(data['Content']).index(str(parts))
            price_1 = str(data['Content'][index+1]).replace(",", ".", 1)
            price_1 = price_1.replace(" ", "")
            price_1 = price_1.replace("Руб.", "")
            price_1 = price_1.replace("=", "")
            
            price_2 = str(data['Content'][index-1]).replace(",", ".", 1)
            price_2 = price_2.replace(" ", "")
            price_2 = price_2.replace("Руб.", "")
            price_2 = price_2.replace("=", "")
            
            price_3 = str(data['Content'][-1]).replace(",", ".", 1)
            price_3 = price_3.replace(" ", "")
            price_3 = price_3.replace("Руб.", "")
            price_3 = price_3.replace("=", "")
            
            try:
                price_1 = float(price_1)
            except:
                price_1 = 0
            try:
                price_2 = float(price_2)
            except:
                price_2 = 0
            try:
                price_3 = float(price_3)
            except:
                price_3 = 0
            
            price = max(price_3, price_1, price_2)
                        
            context['ocr_result'] = price
            
            hotel_instance.hotel_Main_Img = image_file
            hotel_instance.save()

            context['form'] = form
            return render(request, 'scaner.html', context)
    else:
        form = HotelForm()
    
    context['form'] = form
    return render(request, 'scaner.html', context)

def success(request):
    return HttpResponse('successfully uploaded')

def homepage(request):
    form = HomepageForm(request.POST, request.FILES)
    return render(request, 'homepage.html', {'form': form})


def profile(request):
    form = ProfileForm(request.POST, request.FILES)
    return render(request, 'profile.html', {'form': form})