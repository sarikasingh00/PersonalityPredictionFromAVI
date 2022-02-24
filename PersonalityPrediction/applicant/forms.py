from django import forms
from user.models import Applicant
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ApplicantResumeForm(forms.ModelForm):
	class Meta:
		model = Applicant
		fields = ['resume']


class ApplicantAVIForm(forms.ModelForm):
	class Meta:
		model = Applicant
		fields = ['avi']