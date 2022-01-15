from django.shortcuts import render,redirect
from user.models import Applicant,Recruiter
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

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