from django import forms
from .models import Scaner, User, Session
from django.contrib.auth.forms import UserCreationForm


class ScanerForm(forms.ModelForm):

    class Meta:
        model = Scaner
        fields = ['scaner_img']


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username']


class HomepageForm(forms.ModelForm):

    class Meta:
        model = User
        fields = "__all__"


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = "__all__"


class LocalcheckForm(forms.ModelForm):

    class Meta:
        model = User
        fields = "__all__"


class SessionForm(forms.ModelForm):

    class Meta:
        model = Session
        fields = ('users_id',)
        widgets = {
            'members': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')
