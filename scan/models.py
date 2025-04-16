from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# models.py
class Hotel(models.Model):
	User
	name = models.ForeignKey(User, on_delete=models.CASCADE)
	hotel_Main_Img = models.ImageField(upload_to='images/')
