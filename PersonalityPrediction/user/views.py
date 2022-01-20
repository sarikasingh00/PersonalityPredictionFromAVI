from django.shortcuts import render,redirect
from user.models import Applicant,Recruiter
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .forms import UserRegisterForm, ApplicantRegisterForm

# Create your views here.
def recruiter_check(user):
	# return user.is_superuser
	recruiter = Recruiter.objects.filter(user=user).first()
	if recruiter:
		return True
	else:
		return False

def home(request):
	if Recruiter.objects.filter(user=request.user).first():
		print("recruiter")
		return render(request,"recruiter/recruiter_home.html")
	else:
		print("applicant")
		# return render(request,"applicant/applicant_home.html")
		return redirect('applicant-home')


def register(request):
	if request.method == 'POST':
		user_form = UserRegisterForm(request.POST)
		member_form = ApplicantRegisterForm(request.POST)
		if member_form.is_valid() and user_form.is_valid():
			user = user_form.save()
			member =  member_form.save(commit=False)
			member.user = user
			member.save()
			messages.success(request, f'Registration complete! You may log in!')
		else:
			messages.error(request, f'Registration error!')
		return redirect('login')

	else:
		user_form = UserRegisterForm(request.POST)
		applicant_form = ApplicantRegisterForm(request.POST)
	return render(request, 'user/register.html', {'user_form': user_form, 'member_form': applicant_form, 'form_type':'register'})


def welcome_page(request):
	if request.method == 'GET':
		return render(request,"user/welcome.html")
