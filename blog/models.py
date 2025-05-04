from django.db import models
from main.models import Teacher, Department, StudyField
from django_jalali.db import models as jmodels
# Create your models here.

class Post_Teacher(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    lesson_name = models.CharField(max_length=100)
    lesson_type = models.CharField(max_length=100)
    teacher_delay = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default="None-department")
    study_field = models.ForeignKey(StudyField, on_delete=models.CASCADE)
    class_date = jmodels.jDateTimeField()
    class_time = models.TimeField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}  -  {self.tracher}"
