# Generated by Django 5.0.4 on 2024-09-07 11:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0017_alter_davomat_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='davomat',
            name='date',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.date'),
        ),
    ]
