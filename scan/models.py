from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# models.py
class Hotel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    hotel_Main_Img = models.ImageField(upload_to='images/')


class Bill(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_bills')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

class BillParticipant(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    share_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    payment_link = models.URLField(blank=True, null=True)

class LocalCheck(models.Model):
    numbers_of_dishes = models.CharField(max_length=3)
    price_of_one_dish = models.CharField(max_length=6)
    numbers_of_one_dish = models.CharField(max_length=3)

class Session(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_author")
    users_id = models.ManyToManyField(User, related_name="users_id")
    price = models.CharField(max_length=10000000)
