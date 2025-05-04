from django.shortcuts import render, get_object_or_404
from main.models import Teacher, Student, Department, StudyField
from blog.models import Post_Teacher
from blog.forms import PostForm_teacher
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import redirect

# Create your views here.

# بغذ از لاگین کردن پروفایل در این ویو نمایش داده میشود
@login_required(login_url='/')
def teacher_profile_view(request, teacher_id):

    teacher = get_object_or_404(Teacher, pk=teacher_id)


    if teacher.user.id != request.user.id:
        return HttpResponseForbidden("Noooo")
    
    return render(request, 'blog/teacher_profile.html', {'teacher':teacher, 'teacher_id':teacher.id})


# بغذ از لاگین کردن پروفایل در این ویو نمایش داده میشود
@login_required(login_url='/')
def student_profile_view(request, student_id):

    student = get_object_or_404(Student, pk=student_id)
   
    print("-------------------Information---------------------")
    print(f"Student User ID: {student.user.id}")
    print(f"Request User ID: {request.user.id}")
    
    if student.user.id != request.user.id:
        return HttpResponseForbidden(" Noooooo")

    return render(request, 'blog/student_profile.html', {'student':student})


# این ویو فقط مربوط به دکمه آپلود پست هست و کاربر رو به اون یو ار ال منتقل میکنه
# به صفحه آپلود پست میبره
@login_required
def go_to_upload_post(request, teacher_id):
    form = PostForm_teacher(request.POST) 
    teacher = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'blog/upload_post.html', {'form':form ,'teacher':teacher })

# آپلود پست 
@login_required
def upload_post(request, teacher_id):
    current_time = timezone.now()
    teacher = get_object_or_404(Teacher, id=teacher_id)

    form = PostForm_teacher() 
    if request.method == "POST":
        form = PostForm_teacher(request.POST)
        if form.is_valid():
         
            aPost = form.save(commit=False)
            aPost.teacher = teacher

            department_model = get_object_or_404(Department, name=teacher.department)
            aPost.department = department_model

            study_model = get_object_or_404()

            aPost.save()
            return HttpResponse('<h1 style="color:green"> Completed </h1>')
        else:
            return HttpResponse(f"<h1> {form.errors} </h1>")
            return render(request, 'blog/upload_post.html', {'form':form, 'teacher':teacher, 'teacher_id':teacher_id})
    # IF Get Request
    else:
        form = PostForm_teacher(request.POST)
        return render(request, 'blog/upload_post.html', {'form':form, 'teacher':teacher, 'teacher_id':teacher_id})



    return render(request, 'blog/upload_post.html', {'form':form, 'current_time':current_time})

