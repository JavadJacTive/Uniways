from django import forms
from django.core.exceptions import ValidationError
from auth_manager.models import PhoneOTP, PhoneOTP_teacher

class SmsLogin(forms.ModelForm):

    class Meta:
        model = PhoneOTP
        fields = ['is_verified']



class Sms_signUp_teacher(forms.ModelForm):

    class Meta:
        model = PhoneOTP_teacher
        fields = ['is_verified']