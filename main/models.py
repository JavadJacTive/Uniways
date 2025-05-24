from django.db import models
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels

# Create your models here.

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100, blank=False, null=True)
    last_name = models.CharField(max_length=100, blank=False, null=True)
    number = models.CharField(max_length=30)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    field_of_study = models.ForeignKey('StudyField', on_delete=models.SET_NULL, null=True, blank=True)
    education_level = models.ForeignKey('EducationLevel', on_delete=models.SET_NULL, null=True, blank=True)
    password = models.CharField(max_length=128)
    
    verification_phonenumber = models.CharField(max_length=5, default='False') # احراز شماره
    verification_teacher = models.CharField(max_length=20, default='pending') 
    is_active = models.BooleanField(default=True, help_text="آیا کاربر میتواند در سایت فعالیت کند یا خیر")

    # date and time
    create_at_jalali = jmodels.jDateTimeField(auto_now_add=True)
    create_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.first_name + " " + self.last_name 

   
   
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)  # تغییر به ForeignKey
    field_of_study = models.ForeignKey('StudyField', on_delete=models.SET_NULL, null=True, blank=True)
    education_level = models.ForeignKey('EducationLevel', on_delete=models.SET_NULL, null=True, blank=True)
    password = models.CharField(max_length=128)
    
    # اگر فالز باشد کاربر دیگه وجود نداره توی سایت         
    verification_phonenumber = models.CharField(max_length=5, default='False') # اگر فالز بود یعنی کاربر ثبت نام نکرده یا کاربر غیر فعاله یا احراز هویت نشده
    is_active = models.BooleanField(default=True, help_text="آیا کاربر میتواند در سایت فعالیت کند یا خیر") 

    # date and time
    create_at_jalali = jmodels.jDateTimeField(auto_now_add=True)
    create_at = models.DateTimeField(auto_now_add=True)
   

    def __str__(self):
        return "Full Name: " + self.name


class Department(models.Model):
    name = models.CharField(max_length=150)

    # date and time
    create_at_jalali = jmodels.jDateTimeField(auto_now_add=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  self.name

    
class StudyField(models.Model):
    name = models.CharField(max_length=100, default="Unknown")\
    
    # date and time
    create_at_jalali = jmodels.jDateTimeField(auto_now_add=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class EducationLevel(models.Model):
    name = models.CharField(max_length=100, default="کاردانی")

    # date and time
    create_at_jalali = jmodels.jDateTimeField(auto_now_add=True)
    create_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.name