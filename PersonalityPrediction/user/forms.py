from django import forms
from user.models import Applicant
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
	# email=forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']


class ApplicantRegisterForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['is_type']

		
class ApplicantEditForm(forms.ModelForm):
	class Meta:
		model = Applicant
		fields = ['key_skills', 'phone_number', 'profile_pic']