from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
is_type = (
	('Applicant','Applicant'),
	('Recruiter','Recruiter'),
	)

def get_upload_path(instance, filename):
	name = "uploads/%s/%s" % (instance.user.username, filename)
	return name


class Applicant(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE) # username password email first_name last_name
	is_type = models.CharField(max_length=50,choices=is_type,default='Applicant')
	# resume file
	resume = models.FileField(upload_to=get_upload_path , max_length=254) # uploads to media_root/uploads/username/

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
		

	def __str__(self):
		return self.user.first_name

class Recruiter(models.Model):

	user = models.ForeignKey(User, on_delete = models.CASCADE)
	is_type = models.CharField(max_length=50,choices=is_type,default='Applicant')
	

	def __str__(self):
		return self.user.first_name