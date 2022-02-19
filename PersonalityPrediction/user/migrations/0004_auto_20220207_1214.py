# Generated by Django 3.1.7 on 2022-02-07 06:44

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20220207_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='profile_pic',
            field=models.ImageField(default='empty_profile.png', upload_to=user.models.get_profile_upload_path),
        ),
    ]
