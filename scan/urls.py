from django.urls import path
from . import views

urlpatterns = [
    path('livefe/', views.livefe, name='livefe'),
    path('capture_photo/', views.capture_photo, name='capture_photo'),
    path('find_camera_index/', views.find_camera_index, name='find_camera_index'), #Добавляем
    path('start_camera/', views.start_camera, name='start_camera'), #Добавляем
]