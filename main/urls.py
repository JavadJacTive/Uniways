from django.urls import path
from main.views import index, student_sing_up_view, teacher_sing_up_view, pending_teacher_view, approve_teacher, teacher_login_view, student_login_view
from blog.views import teacher_profile_view, student_profile_view
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', index, name='index'),
    path('student/sign/', student_sing_up_view, name='student_sing_up_name'),
    path('student/login/', student_login_view, name= 'student_login_view_name'),
    path('student/profile/<int:student_id>/', student_profile_view, name='student_profile_name'),

    path('teacher/sign/', teacher_sing_up_view, name='teacher_sing_up_name'),
    path('teacher/login/', teacher_login_view, name='teacher_login_view_name'),
    path("teacher/profile/<int:teacher_id>",  teacher_profile_view, name="teacher_profile_name"),

    path('admin_dashboard/', pending_teacher_view, name='pending_teacher_name'),
    path('approve_teacher/<int:teacher_id>/', approve_teacher, name='approve_teacher_name'),

    

    # Logout Student
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout_student_name'),
    
    # Logout teacher
    path('logout_teacher/', auth_views.LogoutView.as_view(next_page='/'), name='logout_teacher_name')
   
]