from django.contrib.auth import login  # اضافه کردن این خط
from django.shortcuts import render, redirect, HttpResponseBadRequest
from django.utils.timezone import now
from .models import Student, PhoneOTP
from django.contrib.auth.models import User

def Student_Verification_SignUp_SMS(request):
    student_id = request.session.get('student_id')
    student_model = Student.objects.get(pk=student_id)

    print(f"\n\n Student_Verification_SignUp_SMS \n student_model: {student_model.number}")

    if request.method == 'POST':
        form_sms = SmsLogin(request.POST)

        if form_sms.is_valid():
            student_sms_status = PhoneOTP.objects.get(phone_number=str(student_model.number))
            sms_code_input = request.POST.get('sms_code_sign_up_input')

            print(f"\n \n  /////////////////// expired_at : {student_sms_status.expired_at.time()} //////////////////")
            print(f"\n /////////////////// now : {now().time()} //////////////////\n \n")
            print(f"\n /////////////////// sms_code_input : {sms_code_input} //////////////////\n \n")

            # چک کردن زمان انقضا و کد SMS
            if now().time() < student_sms_status.expired_at.time() and str(sms_code_input) == str(student_sms_status.otp):
                print("Doroster Dadalshh-----------\n------\n---------\n------\n----\n-----\n------")

                # ساخت کاربر جدید
                user = User.objects.create_user(
                    username=student_model.number,
                    password=student_model.password
                )

                # ثبت نهایی دانشجو
                student_model.user = user
                student_model.verification_phonenumber = "True"
                student_model.save()

                # لاگین کردن کاربر
                login(request, user)  # این خط رو اضافه کن!

                # ریدایرکت به پروفایل
                return redirect("student_profile", student_id=student_id)  # مطمئن شو "student_profile" توی urls.py تعریف شده

            else:
                if now().time() >= student_sms_status.expired_at.time():
                    return render(request, 'auth_manager/sms_student_sign_up.html', {'error_message': "زمان کد تایید منقضی شده؛ لطفا دوباره درخواست بدین *\n روی دکمه کد تایید بزنید"})
                elif str(sms_code_input) != str(student_sms_status.otp):
                    return render(request, 'auth_manager/sms_student_sign_up.html', {'error_message': "کد تایید اشتباه است"})

        return HttpResponseBadRequest("فرم نامعتبر است: " + str(form_sms.errors))

    # اگه GET باشه (اختیاری)
    return render(request, 'auth_manager/sms_student_sign_up.html')