from django import forms
from .models import Hotel, User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class HotelForm(forms.ModelForm):

    class Meta:
        model = Hotel
        fields = ['hotel_Main_Img']


class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']



class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username']