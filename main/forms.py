from django import forms
from main.models import Student, Teacher, Department, StudyField, EducationLevel
from django.core.exceptions import ValidationError
import re

class StudentForm(forms.ModelForm):
    
  
    name = forms.CharField(required=True, error_messages={'required': '🡷 لطفا نام خود را وارد کنید 🡷'})
    number = forms.CharField(required=True, error_messages={'required': ' 🡷 لطفا شماره خود را وارد کنید 🡷'})
    email = forms.CharField(required=True,  error_messages={'required': ' 🡷 لطفا ایمیل  خود را وارد کنید 🡷'})
    password = forms.CharField(required=True,  error_messages={'required': 'لطفا رمز  خود را وارد کنید'})
    
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=True,
        error_messages={'required': "لطفا دانشکده خود را انتخاب کنید"}
    )


    field_of_study = forms.ModelChoiceField(
        queryset=StudyField.objects.all(),
        required=True,
        error_messages={'required': "لطفا رشته خود را انتخاب کنید"}
    )
    
    education_level = forms.ModelChoiceField(
        queryset=EducationLevel.objects.all(),
        required=True,
        error_messages={'required': "لطفا مقطع تحصیلی خود را انتخاب کنید"}
    )
    

    class Meta:
        model = Student
        fields = ['name', 'number', 'email', 'department',  'field_of_study', 'education_level', 'password']
        
    
    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()

        if len(name) > 20 :
            raise ValidationError("طول نام وارد شده خیلی زیاد است")

        return name

   
    def clean_number(self):
        number = self.cleaned_data.get('number', '').strip()

        # Regex
        pattern = r'^09\d{9}$'
        
        # بررسی وجود داشتن فیلد شماره و برگردوندن ارور در فایل ساین آپ فرانت
        if Student.objects.filter(number=number, verification_phonenumber='True').exists():
            raise ValidationError(f"شماره ای که وارد کردین از قبل ثبت نام شده است. <br> شماره‌ای که وارد کردی: {number}")

        # بررسی فرمت شماره
        if not re.match(pattern, number):
            raise ValidationError(f"فرمت اشتباه است! فرمت صحیح: 09123456789 <br> چیزی که وارد کرده بودی: {number}")
        
        

        return number
    
    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        
        
        if len(email) > 50:
            raise ValidationError("طول ایمیلی که وارد کردی خیلی زیاده")
        
        return email

    


class StudentForm_login(forms.Form):

    number = forms.CharField(label='شماره موبایل', required=True, error_messages={'required': 'لطفا شماره موبایل خود را وارد کنید.'})
    password = forms.CharField(widget=forms.PasswordInput, required=True, error_messages={'required': 'لطفا رمز خود را وارد کنید.'})


   
    def clean_number(self):
        
        # get number in html file (main/student_login.html)
        number = self.cleaned_data.get("number").strip()
        # Regex
        pattern = r'^09\d{9}$'

      

        # بررسی فرمت ریجکس
        if not re.match(pattern, number):
            raise ValidationError(f"فرمت اشتباه است! فرمت صحیح: 09123456789 <br> چیزی که وارد کرده بودی: {number}")

        if number.isdigit() == False:
            # منظور از code="only_number"
            # در واقع ما از کد استفاده میکنیم تا اینو توی فرانت صدا بزنیم
            raise ValidationError("شماره موبایل  فقط شامل اعداد باشد", code="only_number")
        
    # بررسی کل فرم (برای درستی اطلاعات)
    # def clean(self):
    #     cleaned_data = super().clean()

    #     if 'number' in self.errors:
    #         return cleaned_data  


    #     number = cleaned_data.get("number")
    #     password = cleaned_data.get("password")
        
    #     # # بررسی در دیتابیس
    #     # student = Student.objects.filter(number=number).first()
        
    #     # if not student or student.password != password:
    #     #     raise ValidationError("شماره یا رمز عبور اشتباه است.")
            

class TeacherForm(forms.ModelForm):
    education_level = forms.ModelChoiceField(
        queryset=EducationLevel.objects.all(),
        required=True,
        error_messages={'required': "لطفا مقطع خود را انتخاب کنید"}
    )

    field_of_study = forms.ModelChoiceField(
        queryset=StudyField.objects.all(),
        required=True,
        error_messages={'required': "لطفا رشته خود را انتخاب کنید"}
    )
  

    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=True,
        error_messages={'required': "لطفا دانشکده خود را انتخاب کنید"}

    )





    

    class Meta:
        model = Teacher 
        fields = ['first_name', 'last_name', 'department', 'field_of_study', 'education_level', 'number', 'password']

   
  
    
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '').strip()

        if len(str(first_name)) > 12:
            raise forms.ValidationError("طول کاراکتر های نام شما زیاد است حداکثر: 10 کاراکتر")

        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '').strip()

        if len(str(last_name)) > 12:
            raise forms.ValidationError("طول کاراکتر های نام‌خانوادگی شما زیاد است حداکثر: 10 کاراکتر")
        
        return last_name
    
    def clean_password(self):
        password = self.cleaned_data.get('password', '').strip()

        if len(str(password)) > 85:
            raise forms.ValidationError("طول کاراکتر های رمز شما زیاد است حداکثر: 120 کاراکتر")

        return password
    
    def clean_number(self):
        number = self.cleaned_data.get('number', '').strip()
        pattern = r'^09\d{9}$'
        
        # فقط اگر شماره با verification_phonenumber='True' وجود داشته باشد، خطا بده
        if Teacher.objects.filter(number=number, verification_phonenumber='True').exists():
            raise ValidationError(f"شماره ای که وارد کردین از قبل ثبت نام شده است. <br> شماره‌ای که وارد کردی: {number}")
        
        # بررسی فرمت شماره
        if not re.match(pattern, number):
            raise ValidationError(f"فرمت اشتباه است! فرمت صحیح: 09123456789 <br> چیزی که وارد کرده بودی: {number}")
        
        return number

class TeacherForm_login(forms.Form):
    
   
    number = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

    # برای اعتبار سنجی کل فرم
    def clean(self):
        cleaned_data = super().clean()

        # get data
        number = cleaned_data.get("number")
        password = cleaned_data.get("password")

        teacher = Teacher.objects.filter(number=number).first()

        if not teacher or teacher.password != password:
            raise ValidationError("شماره یا رمز عبور شما اشتباه است!")

        return cleaned_data
            
    

     