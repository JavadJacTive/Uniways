from django import forms
from blog.models import Post_Teacher
from jalali_date.widgets import AdminJalaliDateWidget
from jalali_date.fields import JalaliDateField

# new





class PostForm_teacher(forms.ModelForm):

    lesson_type = forms.ChoiceField(
        choices=[('both', 'عمومی و تخصصی') ,('general' ,'عمومی'),  ('special', 'تخصصی')]
    )

    teacher_delay = forms.ChoiceField(
        choices=[('choice', 'یک گزینه را انتخاب کنید.'),
                 ('now', 'کلاس درحال برگذاری'),
                 ('5', '5 دقیقه تاخیر'),
                 ('10', '10 دقیقه تاخیر'),
                 ('15', '15 دقیقه تاخیر'),
                 ('20', '20 دقیقه تاخیر'),
                 ('25', '25 دقیقه تاخیر'),
                 ('30', '30 دقیقه تاخیر')
                ]
    )

    class_time = forms.TimeField(label="ساعت کلاس", widget=forms.TimeInput(attrs={'type':'time', 'step':'60'}, format='%H:%M'))

    class Meta:
        model = Post_Teacher    
        fields = ['title', 'lesson_name', 'class_date', 
                   'class_time', 'description', 'lesson_type', 'teacher_delay']

    def __init__(self, *args, **kwargs):
        super(PostForm_teacher,self).__init__(*args, **kwargs)
        self.fields["class_date"]=JalaliDateField(label=("تاریخ کلاس"), widget=AdminJalaliDateWidget)
        self.fields["class_date"].widget.attrs.update({'class':'form-control'})
        self.fields["class_time"].widget.attrs.update({'class':'form-control'})
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['lesson_type'].widget.attrs.update({'class': 'select-dropdown'})
        self.fields['lesson_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['teacher_delay'].widget.attrs.update({'class': 'select-dropdown'})
        

        
        