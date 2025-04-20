from django.http import HttpResponse
from .models import Session, User
from django.contrib.auth.decorators import login_required
from .forms import (
    ScanerForm,
    HomepageForm,
    LocalcheckForm,
    UserUpdateForm,
    SessionForm,
)
from PIL import Image
from django.http import Http404
from apple_ocr.ocr import OCR
from django.shortcuts import render, redirect


KEYWORDS = [
    'сумма',
    'итог',
    'загальна',
    'всего',
    'total',
    'sum',
    'amount',
    'due',
    'balance',
    'итого к оплате:',
    'к оплате',
    'итого:',
]


def scanning_and_dividing(request, pk):
    context = {}
    session = Session.objects.get(pk=pk)
    try:
        session = Session.objects.get(pk=pk)
        count_users = session.users_id.count()
        context['count_users'] = count_users
        if request.method == 'POST':
            form = ScanerForm(request.POST, request.FILES)
            if form.is_valid():
                scaner_instance = form.save(commit=False)
                scaner_instance.user = request.user
                scaner_instance.session_id = session

                image_file = request.FILES['scaner_img']
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
                context['ocr_base_result'] = int(price)
                price = price / count_users
                context['ocr_result'] = int(price)

                scaner_instance.scaner_img = image_file
                scaner_instance.save()

                context['form'] = form
                return render(request, 'scaner.html', context)
        else:
            form = ScanerForm()

        context['form'] = form
        context['session'] = session
        return render(request, 'scaner.html', context)

    except Session.DoesNotExist:
        raise Http404("Сессия не найдена")


def success(request):
    if request == 200:
        return HttpResponse('successfully uploaded')


def homepage(request):
    form = HomepageForm(request.POST, request.FILES)
    return render(request, 'homepage.html', {'form': form})


def local_check(request):
    form = LocalcheckForm(request.POST, request.FILES)
    return render(request, 'localcheck.html', {'form': form})


@login_required
def profile(request):
    sessions = Session.objects.filter(author=request.user)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('scan:profile')
    else:
        form = UserUpdateForm(instance=request.user)

    context = {
        'form': form,
        'sessions': sessions
    }
    return render(request, 'profile.html', context)


@login_required
def session(request):
    user_sessions = Session.objects.filter(users_id=request.user) | Session.objects.filter(author=request.user)
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.author = request.user
            session.save()
            form.save_m2m()
            print("Session сохранена:", session.id)
            return redirect('scan:image_upload', pk=session.id)
        else:
            print("Ошибки формы:", form.errors)
    else:
        form = SessionForm()
    return render(
        request,
        "session.html",
        {'form': form, 'user_sessions': user_sessions.distinct}
    )
