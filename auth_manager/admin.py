from django.contrib import admin
from auth_manager.models import PhoneOTP, PhoneOTP_teacher


# Register your models here.

class OtpAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'otp', 'expired_at')

class OtpTeacherAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'otp', 'expired_at')

admin.site.register(PhoneOTP, OtpAdmin)
admin.site.register(PhoneOTP_teacher, OtpTeacherAdmin)