import os
from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.forms import CharField
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

# Create your models here.
is_type = (
	('Applicant','Applicant'),
	('Recruiter','Recruiter'),
	)

def get_resume_upload_path(instance, filename):
	name = "uploads/%s/resume/%s" % (instance.user.username, filename)
	return name

def get_profile_upload_path(instance, filename):
	name = "uploads/%s/profile/%s" % (instance.user.username, filename)
	# print(name)
	return name

def get_avi_upload_path(instance, filename):
	name = "uploads/%s/avi/%s" % (instance.user.username, filename)
	return name


class Applicant(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE) # username password email first_name last_name
	is_type = models.CharField(max_length=50,choices=is_type,default='Applicant')
	# resume file
	resume = models.FileField(upload_to=get_resume_upload_path , max_length=254) # uploads to media_root/uploads/username/resume/
	profile_pic = models.ImageField(upload_to=get_profile_upload_path, max_length=100, default = 'empty_profile.png') # uploads to media_root/uploads/username/profile/
	avi = models.FileField(upload_to=get_avi_upload_path , max_length=254, blank=True, null=True) # uploads to media_root/uploads/username/avi
	# contact_no = models.IntegerField(max_length=10)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
	key_skills = models.JSONField(default=list)
	

	# TODO: link to AVI 
	
	# personality scores OCEAN
	o = models.FloatField(null=True, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],blank=True)
	c = models.FloatField(null=True, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],blank=True)
	e = models.FloatField(null=True, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],blank=True)
	a = models.FloatField(null=True, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],blank=True) 
	n = models.FloatField(null=True, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],blank=True)
	
	# posts applied for
	SOFTWARE_ENGINEER = 'SWE'
	FRONTEND_DEV = 'Frontend Developer'
	BACKEND_DEV = 'Backend Developer'
	DATA_SCIENTIST = 'Data Scientist'
	MACHINE_LEARNING_ENGINEER= 'Machine Learning Engineer'
	 
	POST_CHOICES = [
        (SOFTWARE_ENGINEER, 'SWE'),
    	(FRONTEND_DEV,'Frontend Developer'),
    	(BACKEND_DEV,'Backend Developer'),
        (DATA_SCIENTIST,'Data Scientist'),
        (MACHINE_LEARNING_ENGINEER,'Machine Learning Engineer'),
    ]
	applied_posts = models.CharField(
		max_length=50,
        choices=POST_CHOICES,
        default=SOFTWARE_ENGINEER,
    )

	def resume_filename(self):
		return os.path.basename(self.resume.name)	

	
	def profile_filename(self):
		return os.path.basename(self.profile_pic.name)

	def avi_filename(self):
		return os.path.basename(self.avi.name)

	def __str__(self):
		return self.user.first_name


class Recruiter(models.Model):

	user = models.ForeignKey(User, on_delete = models.CASCADE)
	is_type = models.CharField(max_length=50,choices=is_type,default='Applicant')
	

	def __str__(self):
		return self.user.first_name