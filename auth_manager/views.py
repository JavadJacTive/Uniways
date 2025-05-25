from django.shortcuts import render, redirect
from django.http import JsonResponse 
import requests 
from django.contrib.auth.models import User
from main.forms import StudentForm
from auth_manager.forms import SmsLogin, Sms_signUp_teacher
from django.http import HttpResponseBadRequest
from auth_manager.models import PhoneOTP
from datetime import timedelta
from django.utils import timezone
from auth_manager.models import PhoneOTP, PhoneOTP_teacher
from django.utils.timezone import now
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from main.models import Student, Teacher
from melipayamak import Api
from django.contrib.auth import login
import random

# Create your views here.


# این ویو فقط کاربر رو منتقل میکنه به صفحه اجراز هویت 
def Student_Send_Code_SignUp_SMS(request):
    
    
    return render(request, 'auth_manager/sms_student_sign_up.html')



def Send_SMS(request):
    
    # گزفتن آیدی از قرم قبلی با سشن
    student_id = request.session.get('student_id')
    print(f"Diiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiir: {student_id}")

    # پیدا کردن رکورد با آیدی و استفاده از فیلدهاش در خط های بعدی
    student = Student.objects.get(pk=student_id)
    print(f"student.number: {student.number}")

    import requests, random
    
    if request.method == 'POST':
        # دریافت داده‌ها از POST
        name = request.POST.get('name')
        print(f'deeer: {name}')

    generate_random_code = random.randint(1000, 9999)

    # مثلا کد اس ام اس
    
    try:
        username = '09931567815'
        password = '6!#ML'
        api = Api(username,password)
        sms_soap = api.sms('soap')
        sms_soap.send_by_base_number(f"{generate_random_code}", f'{student.number}'.strip(), 308145)
    except:
        pass
        print("Errore")

    # آپدیت کردن دیتابیس 
    # هربرا که کاربر با یه شماره درخواست کد میده میاد اینجا و کدش ذخیره میشه
    PhoneOTP_user, created = PhoneOTP.objects.update_or_create(
    phone_number=student.number,
        defaults={
            "otp": str(generate_random_code),
            "expired_at": timezone.now() + timedelta(minutes=1),
        }
    )

    return JsonResponse({'message': 'کد تایید ارسال شد!'})


# این ویو بررسی میکنه اگه ثبت اطلاعات و اجراز هویت هر دو درست بودند ثبت نام رو نهایی کنه
def Student_Verification_SignUp_SMS(request):

    # گرفتن آیدی از فرم با سشن
    student_id = request.session.get('student_id')
    
     # پیدا کردن رکورد با آیدی و استفاده از فیلدهاش در خط های بعدی
    student_model = Student.objects.get(pk=student_id)

    
    print(f"\n\n Student_Verification_SignUp_SMS \n student_model: {student_model.number}")
    
    if request.method == 'POST':

        # گرفتن فرم اس ام اس در حال 
        form_sms = SmsLogin(request.POST)
        
       
        if form_sms.is_valid():
            
            # پیدا کردن فیلد اون شخص با شمارش
            student_sms_status = PhoneOTP.objects.get(phone_number=str(student_model.number))
            # گرفتن ورودی در اچ تی ام ال اون چیزی که کاربر وارد کرده
            number1_student = request.POST.get('number1_student')
            number2_student = request.POST.get('number2_student')
            number3_student = request.POST.get('number3_student')
            number4_student = request.POST.get('number4_student')
            numbers = number1_student+number2_student+number3_student+number4_student

            print(f"\n \n  /////////////////// expired_at : {student_sms_status.expired_at.time()} //////////////////")
            print(f"\n /////////////////// now : {now().time()} //////////////////\n \n")
            print(f"\n /////////////////// sms_code_input : {number1_student+number2_student+number3_student+number4_student} //////////////////\n \n")

            # اگر تایم در حال حاضر کوچک تر از تایم انقضا بود بیا و کاربر رو ثبت کن
            # و همچنین اگر کد تایید برابر همون گد تایید خاص بود
            if now().time() < student_sms_status.expired_at.time() and str(numbers) == str(student_sms_status.otp):
                print("Doroster Dadalshh-----------\n------\n---------\n------\n----\n-----\n------")

             
             

                # ساختن یوزر جدید 
                user = User.objects.create_user(
                    username=student_model.number,
                    password=student_model.password
                )
                
                # ثبت یک یوزر جدید
                # ثبت نهایی
                student_model.user = user
                student_model.verification_phonenumber = "True"
                student_model.save()

                 # لاگین کردن کاربر
                login(request, user)
                
                return redirect("student_profile_name", student_id=student_id)
            
            # بررسی ارور ها
            else:
                
                if now().time() >= student_sms_status.expired_at.time():
                    return render(request, 'auth_manager/sms_student_sign_up.html', {'error_message': "زمان کد تایید منقضی شده؛ لطغا دوباره درخواست بدین *\n روی دکمه کد تایید بزنید"})
                
                elif str(numbers) != str(student_sms_status.otp):
                    return render(request, 'auth_manager/sms_student_sign_up.html', {'error_message': "کد تایید اشتباه است"})


        
        return HttpResponseBadRequest("فرم نامعتبر است: " + str(form_sms.errors))



#---------------T E A C H E R-----------------#

# این ویو فقط کاربر رو منتقل میکنه به صفحه اجراز هویت 
def Teacher_Send_Code_SignUp_SMS(request):
    return render(request, 'auth_manager/sms_teacher_sign_up.html')


def Send_SMS_teacher(request):
    teacher_id = request.session.get('teacher_id')  
    teacher = Teacher.objects.get(pk=teacher_id)
    print(f"T E A C H E R ID: {teacher_id}")

    generate_random_code = random.randint(1000, 9999)

    try:
        print(100)
        # username = '09931567815'
        # password = '6!#ML'
        # api = Api(username,password)
        # sms_soap = api.sms('soap')
        # sms_soap.send_by_base_number(f"{generate_random_code}", f'{teacher.number}'.strip(), 308145)
    except:
        pass
    
    # Create Record for OTP (create otp & expire otp)
    PhoneOTP_user, created = PhoneOTP_teacher.objects.update_or_create(
        phone_number=teacher.number,
        defaults={
            "otp": str(generate_random_code),
            "expired_at":timezone.now() + timedelta(minutes=1)
        }
    )
    


    return HttpResponse("<h1> SMS </h1>")

# این ویو بررسی میکنه اگه ثبت اطلاعات و اجراز هویت هر دو درست بودند ثبت نام رو نهایی کنه
def Teacher_Verification_SignUp_SMS(request):
    
    teacher_id = request.session.get('teacher_id')
    teacher_model = Teacher.objects.get(pk=teacher_id)
    form_sms = Sms_signUp_teacher(request.POST)

    number1 = request.POST.get('number1_teacher')
    number2 = request.POST.get('number2_teacher')
    number3 = request.POST.get('number3_teacher')
    number4 = request.POST.get('number4_teacher')
    teacher_sms_status = PhoneOTP_teacher.objects.get(phone_number=str(teacher_model.number))
   
    print(f'N U M B E R S  : {number1}{number2}{number3}{number4} \n Generate Code: ')
    numbers = str(number1+number2+number3+number4) # کد تاییدی که کاربر وارد کرده

    if request.method == 'POST':

        # get record Otp
        teacher_sms_status = PhoneOTP_teacher.objects.get(phone_number=str(teacher_model.number))

        print(f"/\/\/\/\/\/\/\/\/\/\/\ numbers:{numbers}>> otp: {teacher_sms_status.otp} \/\/\/\\n ")
        
        #  اگر کد تایید درست بود و اگر هنوز زمن باقی مانده بود
        if now().time() <= teacher_sms_status.expired_at.time() and int(numbers) == int(teacher_sms_status.otp):
            # ساختن یوزر جدید 
            user = User.objects.create_user(
                username=teacher_model.number,
                password=teacher_model.password
            )

            # ثبت یک یوزر جدید
            # ثبت نهایی
            teacher_model.user = user
            teacher_model.verification_phonenumber = "True"
            teacher_model.verification_teacher = "pending"
            teacher_model.save()

            # لاگین کردن کاربر
            login(request, user)
            
            # در ابتدا چون هنوز معلوم نیست که استاد هست یا نه میره به صفحه انتظار
            return render(request, "main/waiting_teacher.html")
        else:
            # اگر زمان کد منقضی شده بود
            if now().time() >= teacher_sms_status.expired_at.time():
                messages.error(request, "کد تایید منقضی شده لطفا دوباره درخواست بدین")
                return render(request, 'auth_manager/sms_teacher_sign_up.html')

            # اگر کد تایید اشتباه یود
            elif int(numbers) != int(teacher_sms_status.otp):
                messages.error(request, "کد تایید اشتباه است")
                return render(request, 'auth_manager/sms_teacher_sign_up.html')
                # return HttpResponse('<h1 style="color:red"> can not Access </h1>')
    
  
    return render(request, 'auth_manager/sms_teacher_sign_up.html')
    