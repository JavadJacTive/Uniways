from django.contrib import admin
from main.models import Student, Teacher, Department, StudyField, EducationLevel


class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'number', 'department', 'field_of_study', 'education_level', 'password', 'create_at_jalali', 'create_at', 'verification_phonenumber', 'is_active')
    search_fields = ('name', 'number', 'email')
    list_filter = ('department',)


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id' ,'first_name', 'last_name', 'number', 'department', 'education_level', 'field_of_study', 'password', 'create_at_jalali', 'create_at', 'verification_teacher', 'verification_phonenumber', 'is_active')
    #search_fields = ('name', 'number', 'email')
    list_filter = ('department',)

class Field_of_study_Admin(admin.ModelAdmin):
    list_display = ('id', 'name', 'create_at_jalali', 'create_at')

class Department_Admin(admin.ModelAdmin):
    list_display = ('id', 'name', 'create_at_jalali', 'create_at')

class EducationLevel_Admin(admin.ModelAdmin):
    list_display = ('id', 'name')

# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Department, Department_Admin)
admin.site.register(StudyField, Field_of_study_Admin)
admin.site.register(EducationLevel, EducationLevel_Admin)
