
# for Farsi Character
import sys
sys.stdout.reconfigure(encoding='utf-8')

from django.shortcuts import render, redirect
from main.forms import StudentForm, TeacherForm, TeacherForm_login, StudentForm_login
from main.models import Department, Teacher, Student, StudyField
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def index(request):
    # اکر کاربر لاگین کرده باشه و شناخته شده باشه
    if request.user.is_authenticated:
        student = Student.objects.filter(user=request.user).first()
        teacher = Teacher.objects.filter(user=request.user).first()
        
        
        print(f"S T U D E N T : {student}")
        # دانشجو ب صفحه پروفایلش بره یا بگه محدود شدید
        if student:
            if student.is_active == False:
                return HttpResponse("<h1> دسترسی شما محدود شده <a href='https://t.me/mohammadjivad'> پشتیبانی </a> </h1>")
            elif student.is_active == True:
                return redirect("student_profile_name", student_id=student.id)
        
        # استاد به صفحه پروفایلش یا صفحه انتظار بره
        # go to waiting page
        if teacher:
            if teacher.verification_teacher == 'pending':
                return render(request, "main/waiting_teacher.html")
            if teacher.verification_teacher == "reject":
                return HttpResponse("<h1> احراز هویت شما رد شده لطفا به پشتیبانی پیام دهید. </h1>")
            if teacher.verification_teacher == "approve":
                return redirect('teacher_profile_name', teacher_id=teacher.id)
                

        
        
    # اگر کاربر لاگین نکرده بود
    return render (request, 'main/index.html')



def pending_teacher_view(request):
    teachers_status = Teacher.objects.filter(verification_teacher='pending')
    return render(request, 'main/Teacher_pending.html', {'teachers_status' : teachers_status})


def approve_teacher(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            teacher.verification_teacher = 'approve'
        elif action == 'reject':
            teacher.verification_teacher = 'reject'
        teacher.save()
    return redirect('approve_teacher_name', teacher_id=teacher_id)


def teacher_sing_up_view(request):
    
    # وقتی درخواست گت رو زد و اومد تو صفحه بیاد از دیتابیس لود بشه
    departments = Department.objects.all()
    studyfields = StudyField.objects.all()

    if request.method == 'POST':
        
        # گرفتن فرم از اسکریپت فرم
        form = TeacherForm(request.POST)

        # اگر فرم ارور نداشت سیو کن
        if form.is_valid():
            departments = Department.objects.all()
            studyfields = StudyField.objects.all()
            

            # ساخت یوزر جدید
            # user = User.objects.create_user(
            #     username=form.cleaned_data["number"],
            #     password=form.cleaned_data["password"]
            # )
            print(" T E A C H E R - F O R M")
            print(f"F O R M : {form.cleaned_data['first_name']}")

            # Save Data in Database
            teacher = Teacher(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                number=form.cleaned_data['number'],
                department=form.cleaned_data['department'],
                field_of_study= "SS",
                password=form.cleaned_data['password'],
                verification_teacher='False'
                )
            teacher.save()

            # save teacher.id to use auth_manager App (views.py)
            request.session['teacher_id'] = teacher.id

            # Save Data in Session
            request.session['first_name_teacher'] = form.cleaned_data['first_name']
            request.session['last_name_teacher'] = form.cleaned_data['last_name']
            request.session['number_teacher_'] = form.cleaned_data['number']
            request.session['department_teacher'] = form.cleaned_data['department']
            request.session['password_teacher'] = form.cleaned_data['password']



            # متصل کردن استاد به یوزر استاد 
            # teacher = form.save(commit=False)
            # teacher.user = user
            # teacher.save()

            
            return redirect("teacher_sms_signUp_Name")
        else:
            print(form.errors)
            return render(request, 'main/teacher_sing_up.html', {'form': form, 'departments':departments, 'studyfields':studyfields})
    # اگر گت بود
    else:
        form = TeacherForm()
        return render(request, 'main/teacher_sing_up.html', {'form': form, 'departments':departments, 'studyfields':studyfields})


def teacher_login_view(request):
    form = TeacherForm_login()

    if request.method == "POST":
        form = TeacherForm_login(request.POST)

        if form.is_valid():
            # دریافت اطلاعات معلم از شماره موبایل (یا هر مشخصه‌ای که در فرم لاگین استفاده شده)
            teacher = Teacher.objects.filter(number=form.cleaned_data["number"]).first()
            
            # چک کنیم که teacher مقدار داشته باشه
            if teacher and teacher.user:

                # اگر استاد ریجکت شده بود 
                if teacher.verification_teacher == "reject":
                    return HttpResponse("<h1> شمار ریجکت شدین لطفا به پشتیبانی پیام بدین </h1>")
                
                if teacher.verification_teacher == "approve":
                        
                    user = teacher.user
                    login(request, user)
                    return redirect("teacher_profile_name", teacher_id=teacher.id)
            else:
                print("Teacher not found")
        else:
            print("Not Oky")

    teacher = None  # مقدار پیش‌فرض برای جلوگیری از خطا
    if request.user.is_authenticated:
        teacher = Teacher.objects.filter(number=request.user.username).first()

    return render(request, 'main/teacher_login.html', {"form": form, "teacher": teacher})




def student_sing_up_view(request):
    
    # وقتی درخواست گت رو زد و اومد تو صفحه بیاد از دیتابیس لود بشه
    department = Department.objects.all()
    studyField = StudyField.objects.all()

    # درخواست پست (برای قرم ثبت نام)
    if request.method == 'POST':

        department = Department.objects.all()
        studyField = StudyField.objects.all()
        
        # گرفتن فرم از اسکریپت فرم
        form = StudentForm(request.POST)
        
        # اگر فرم ارور نداشت سیو کن
        if form.is_valid():

            student_exists = Student.objects.filter(number=request.POST.get('number'), verification_phonenumber='False').exists()
            # اگر دانشجوی اجراز هویت نشده ای پیدا نشد بیاد و یدونه بسازه ازش
            if student_exists == False:

                # ادد کردن اطلاعات به دیتابیس(ولی هنوز اجراز هویت نشده)
                student = form.save(commit=False)
                student.save()

                # سیو کردن آیدی
                # این آیدی رو اینجا سیو میکنیم تا در اپ اس ام اس استفاده کنیم
                request.session['student_id'] = student.id 

                # اگر فرم ولید بود بره به صفحه اس ام اس
                return redirect("student_sms_signUp_Name")
            # اما اگر رکورد دانشجو پیدا شد بیاد اطلاعات فرم رو آپدیت کنه فقط دیگه نسازه تکراری
            if student_exists == True:
                student_record = Student.objects.filter(number=request.POST.get('number'), verification_phonenumber='False').first()
                
                student_record.name = request.POST.get('name')
                student_record.number = request.POST.get('number')

                department_id = request.POST.get('department')
                student_record.department = Department.objects.get(id=department_id)

                field_of_study_id = request.POST.get('field_of_study')
                student_record.StudyField = StudyField.objects.get(id=field_of_study_id)
                
               
                student_record.password = request.POST.get('password')
                student_record.verification_phonenumber = 'False'
                student_record.save()
                return redirect("student_sms_signUp_Name")
        else:
            # اگر فرم ولید نبود برو و توی همون صفحه ارور هارو برگردون
            print(form.errors)
            department = Department.objects.all()
            studyField = StudyField.objects.all()
            return render(request, 'main/student_sing_up.html', {'form': form, 'departments':department, 'studyField':studyField})  # اینجا فرم رو مجدداً رندر می‌کنیم که خطاها نمایش داده بشن
    else:
        # اگه ریکوعست پست نبود و گت بود کار خاصی قرار نیست بکنیم
        form = StudentForm()  # برای درخواست‌های GET، فرم خالی رو رندر می‌کنیم
        department = Department.objects.all()
        studyField = StudyField.objects.all()
        return render(request, 'main/student_sing_up.html', {'form': form, 'departments':department, 'studyField':studyField})
    

from django.http import HttpResponse
def student_login_view(request):
    
    # اگر از قبل لاگین کرده بود مستقیم بره پروفایلش
    if request.user.is_authenticated:
        student = Student.objects.filter(user=request.user).first()
        if student:
            return redirect("student_profile_name", student_id=student.id)



    # فرم رو از استیودنت فرم بگیر به صورت گت
    form = StudentForm_login()
    
    if request.method == "POST":
        # اگر درخواست فرم داد
        form = StudentForm_login(request.POST)
        
        # اگر فرم مغتبر بود و اروری نداشت برو بررسی کن
        if form.is_valid():

            # بررسی در دیتابیس
            student = Student.objects.filter(number=request.POST.get('number')).first()
            print("--------------------Student------------------")
            print(student.number)
            print(student.password)
            
            
            # بر اساس شماره تلفنی که کاربر وارد کرده رکورد رو پیدا کن
            student = Student.objects.filter(number=request.POST.get('number')).first()
          
            user = authenticate(request, username=student.number, password=student.password)
            

            # اگر دانشجو وجود داشت برو و لاگین کن
            if user is not None  :
                login(request, user)
                student = Student.objects.get(user=user)
                return redirect("student_profile_name", student_id=student.id)
                print("Okyyy")

            # اگر مشخصات دانشجو اشتباه بود
            if not student or student.password != request.POST.get('password'):
                print("--------------- not Exist --------------")
                print(f"N O T - E X I S T S : {student} \n PassWordDB: {student.password} \n`` PassWordInput: {request.POST.get('password')}")
                messages.error(request, 'شماره یا رمز عبور اشتباه هست')
                return render(request, 'main/student_login.html')
                

        # اگر فرم ولید نبود
        else:
            return render(request, "main/student_login.html", {"form": form})
        
    student = None  # مقدار پیش‌فرض برای جلوگیری از خطا
    if request.user.is_authenticated:
        student = Student.objects.filter(number=request.user.username).first()

    return render(request, 'main/student_login.html', {"form": form, "student": student})
                


