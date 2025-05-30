# Generated by Django 5.1.6 on 2019-04-05 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_alter_student_field_of_study'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='status',
            new_name='verification_status',
        ),
        migrations.AddField(
            model_name='student',
            name='is_active',
            field=models.BooleanField(default=True, help_text='آیا کاربر میتواند در سایت فعالیت کند یا خیر'),
        ),
    ]
