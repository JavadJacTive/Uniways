from django.db import models
from django.utils import timezone
from datetime import timedelta 

# Create your models here.

class PhoneOTP(models.Model):
    phone_number = models.CharField(max_length=50, unique=False)
    otp = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.phone_number 


class PhoneOTP_teacher(models.Model):
    phone_number = models.CharField(max_length=50, unique=False)
    otp = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return "Test" + self.phone_number 
