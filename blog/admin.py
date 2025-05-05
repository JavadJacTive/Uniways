from django.contrib import admin
from blog.models import Post_Teacher


class Post_teacher_Admin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'lesson_name', 'department', 'study_field', 'class_date', 'lesson_type')


admin.site.register(Post_Teacher, Post_teacher_Admin)