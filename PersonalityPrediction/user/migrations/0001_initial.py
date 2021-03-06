# Generated by Django 3.0.2 on 2022-02-05 07:16

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recruiter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_type', models.CharField(choices=[('Applicant', 'Applicant'), ('Recruiter', 'Recruiter')], default='Applicant', max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_type', models.CharField(choices=[('Applicant', 'Applicant'), ('Recruiter', 'Recruiter')], default='Applicant', max_length=50)),
                ('resume', models.FileField(max_length=254, upload_to=user.models.get_resume_upload_path)),
                ('profile_pic', models.ImageField(upload_to=user.models.get_profile_upload_path)),
                ('phone_number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('o', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
                ('c', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
                ('e', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
                ('a', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
                ('n', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
                ('applied_posts', models.CharField(choices=[('SWE', 'SWE'), ('Frontend Developer', 'Frontend Developer'), ('Backend Developer', 'Backend Developer'), ('Data Scientist', 'Data Scientist'), ('Machine Learning Engineer', 'Machine Learning Engineer')], default='SWE', max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
