# Generated by Django 3.1.7 on 2022-03-07 12:46

import django.core.validators
from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20220307_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='resume',
            field=models.FileField(max_length=254, upload_to=user.models.get_resume_upload_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])]),
        ),
    ]
