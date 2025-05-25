from django.urls import path
from main.views import index, student_sing_up_view, teacher_sing_up_view, pending_teacher_view, approve_teacher, teacher_login_view, student_login_view
from blog.views import teacher_profile_view, student_profile_view
from django.urls import path
from auth_manager.views import Student_Send_Code_SignUp_SMS, Student_Verification_SignUp_SMS, Send_SMS, Teacher_Verification_SignUp_SMS, Teacher_Send_Code_SignUp_SMS, Send_SMS_teacher



urlpatterns = [
    path('student/sign/sms/', Student_Send_Code_SignUp_SMS, name="student_sms_signUp_Name"),
    path('student/sign/sms/verified/', Student_Verification_SignUp_SMS, name="student_sms_signUp_verified_Name"),
    path('send_sms_sign_up/', Send_SMS, name='send_sms_sign_up_name'),

    path('teacher/sign/sms/', Teacher_Send_Code_SignUp_SMS, name="teacher_sms_signUp_Name"), # کاربر رو منتقل میکنه فقط به صفحه اس ام اس
    path('teacher/sign/sms/verified/', Teacher_Verification_SignUp_SMS, name="teacher_sms_signUp_verified_Name"), # چک کردن اس ام اس
    path('send_sms_teacher_sign_up/', Send_SMS_teacher, name="send_sms_teacher_sign_up_name")

]