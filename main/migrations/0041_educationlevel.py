# Generated by Django 5.1.6 on 2025-05-17 13:48

import django_jalali.db.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0040_alter_teacher_department'),
    ]

    operations = [
        migrations.CreateModel(
            name='EducationLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='کاردانی', max_length=100)),
                ('create_at_jalali', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
