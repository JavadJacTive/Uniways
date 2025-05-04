from django.urls import path
from main.views import index, student_sing_up_view, teacher_sing_up_view, pending_teacher_view, approve_teacher, teacher_login_view, student_login_view
from blog.views import teacher_profile_view, student_profile_view, upload_post, go_to_upload_post

urlpatterns = [
    path('teacher/profile/<int:teacher_id>/upload_post', go_to_upload_post, name='upload_post_Page_name'),
    path('teacher/profile/<int:teacher_id>/uploaded_post', upload_post, name='upload_post_name'),
    
]


