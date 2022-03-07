from django.shortcuts import render,redirect
from django.urls import reverse
from user.models import Applicant,Recruiter
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .forms import UserRegisterForm, ApplicantRegisterForm, ApplicantEditForm
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
	print(request.user)
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
	print('login view')
	if request.method == 'POST':
		if request.POST['flag'] == 'login':
			username = request.POST['username']
			password = request.POST['password']
			print(username, password)
			user = authenticate(username=username, password=password)
			print(user)		
			if user is not None:
				# request.session['user'] = user
				login(request, user)
				return redirect('home')
			else:
				print("Login unsuccessful")
				user_form = UserRegisterForm()
				applicant_form = ApplicantRegisterForm()
				messages.error(request, 'Incorrect username or password.')
		elif request.POST['flag'] == 'register' or request.session['old_post'].POST['flag'] == 'register':
			if 'old_post' in request.session:
				user_form = UserRegisterForm(request.session['old_post'])
				member_form = ApplicantRegisterForm(request.session['old_post'])
			else:
				user_form = UserRegisterForm(request.POST)
				member_form = ApplicantRegisterForm(request.POST)
			print(user_form.errors)
			print(member_form.errors)
			if member_form.is_valid() and user_form.is_valid():
				user = user_form.save()
				member =  member_form.save(commit=False)
				member.user = user
				member.save()
				login(request, user)
				messages.success(request, f'Registration complete! You may log in!')
				return redirect('home')
			else:
				messages.error(request, f'Registration error!')
				request.session['old_post'] = request.POST
				return render(request, 'user/register_login.html', {'user_form': user_form, 'member_form': member_form, 'errors':user_form.errors})
				# return redirect('login')
	else:
		# user_form = UserRegisterForm(request.POST)
		print("In get")
		user_form = UserRegisterForm()
		applicant_form = ApplicantRegisterForm()
	return render(request, 'user/register_login.html', {'user_form': user_form, 'member_form': applicant_form, })



def edit_profile(request):
	if request.method=='POST':
		u_form = UserRegisterForm(request.POST, instance = request.user)
		a_form = ApplicantEditForm(request.POST, request.FILES, instance=Applicant.objects.filter(user=request.user).first())
		# p_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)
		if(u_form.is_valid() and a_form.is_valid()):
			u_form.save()
			a_form.save()
			# p_form.save()
			messages.success(request, f'Your account has been updated!')
			login(request,request.user) #IMP
			return redirect(reverse('home'))
	
	else:
		u_form = UserRegisterForm(instance = request.user)
		a_form = ApplicantEditForm(instance = Applicant.objects.filter(user=request.user).first())
		# p_form = ProfileUpdateForm(instance = request.user.profile)
	context = {
	'u_form' : u_form,
	'a_form' : a_form
	}

	return render(request, "user/profile.html", context)



	"""
	Session:
		request[user] - sarikasingh
		change - sarikasingh2
	"""