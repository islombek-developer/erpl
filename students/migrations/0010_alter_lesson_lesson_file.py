# Generated by Django 5.0.4 on 2024-08-23 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0009_rename_homework_file_lesson_lesson_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='lesson_file',
            field=models.FileField(blank=True, null=True, upload_to='lessons'),
        ),
    ]
