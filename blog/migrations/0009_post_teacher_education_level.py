# Generated by Django 5.1.6 on 2025-05-17 14:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_rename_created_at_post_teacher_create_at_and_more'),
        ('main', '0043_student_education_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='post_teacher',
            name='education_level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.educationlevel'),
        ),
    ]
