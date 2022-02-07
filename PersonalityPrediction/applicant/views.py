from django.shortcuts import render, redirect
from django.contrib import messages
from user.models import Applicant
from .forms import ApplicantResumeForm


# Create your views here.
def home(request):
	if request.method == 'GET':
		return render(request,"applicant/applicant_home.html")


def resume_upload(request):
	print("in resume upload view")
	if request.method == 'POST':
		print("in POST")
		resume_file = request.FILES['resume']
		applicant_obj = Applicant.objects.get(user = request.user)
		applicant_obj.resume = resume_file
		try :
			applicant_obj.save()
			messages.success(request, 'Resume Uploaded!')
		except:
			print("Object not saved")
			messages.error(request, 'Upload not successful')
	
		return redirect('home')
	else:
		resume_form = ApplicantResumeForm()
		return render(request,"applicant/upload_resume.html",{'form':resume_form})

def dashboard(request):
	user = request.user
	applicant = Applicant.objects.filter(user=user).first()
	fields = {
		'first_name' : applicant.user.first_name,
		'last_name' : applicant.user.last_name,
		'email' : applicant.user.email,
		'applied_post': applicant.applied_posts,
		'resume': applicant.resume,
	}
	# print(fields)
	return render(request,"applicant/dashboard.html", {'fields':fields})


