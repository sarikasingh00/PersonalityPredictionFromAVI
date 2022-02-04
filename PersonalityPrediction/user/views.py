from django.shortcuts import render,redirect
from user.models import Applicant,Recruiter
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .forms import UserRegisterForm, ApplicantRegisterForm
from django.contrib.auth import authenticate, login

# Create your views here.
def recruiter_check(user):
	# return user.is_superuser
	recruiter = Recruiter.objects.filter(user=user).first()
	if recruiter:
		return True
	else:
		return False

def home(request):
	# print(request.user.is_authenticated)
	if Recruiter.objects.filter(user=request.user).first():
		print("recruiter")
		return render(request,"recruiter/recruiter_home.html")
	else:
		print("applicant")
		# return render(request,"applicant/applicant_home.html")
		return redirect('applicant-home')


# def register(request):
# 	if request.method == 'POST':
# 		user_form = UserRegisterForm(request.POST)
# 		member_form = ApplicantRegisterForm(request.POST)
# 		if member_form.is_valid() and user_form.is_valid():
# 			user = user_form.save()
# 			member =  member_form.save(commit=False)
# 			member.user = user
# 			member.save()
# 			messages.success(request, f'Registration complete! You may log in!')
# 		else:
# 			messages.error(request, f'Registration error!')
# 		return redirect('login')

# 	else:
# 		user_form = UserRegisterForm(request.POST)
# 		applicant_form = ApplicantRegisterForm(request.POST)
# 	return render(request, 'user/register_login.html', {'user_form': user_form, 'member_form': applicant_form, 'form_type':'register'})


def welcome_page(request):
	if request.method == 'GET':
		return render(request,"user/welcome.html")


def register_login(request):
	if request.method == 'POST':
		if request.POST['flag'] == 'login':
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			print(user)		
			if user is not None:
				return redirect('home')
			else:
				print("Login unsuccessful")
		else:
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
	return render(request, 'user/register_login.html', {'user_form': user_form, 'member_form': applicant_form, })

def profile(request):
	if request.method=='POST':
		u_form = UserRegisterForm(request.POST, instance = request.user)
		# p_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)
		if(u_form.is_valid()):
			u_form.save()
			# p_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('profile')
	else:
		u_form = UserRegisterForm(instance = request.user)
		# p_form = ProfileUpdateForm(instance = request.user.profile)
	context = {
	'u_form' : u_form,
	# 'p_form' : p_form
	}

	return render(request, "user/profile.html", context)