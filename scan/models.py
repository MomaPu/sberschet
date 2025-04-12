from django.db import models


# models.py
class Hotel(models.Model):
	name = models.CharField(max_length=50)
	hotel_Main_Img = models.ImageField(upload_to='images/')
