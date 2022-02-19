from django.shortcuts import render, redirect
from django.contrib import messages
from user.models import Applicant
from .forms import ApplicantResumeForm
from pyresparser import ResumeParser

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
			print(applicant_obj.resume.name)
			extract_skills(applicant_obj.resume.name, applicant_obj)
		except Exception as e:
			print("Object not saved", e )
			messages.error(request, 'Upload not successful')
	
		return redirect('home')
	else:
		resume_form = ApplicantResumeForm()
		return render(request,"applicant/upload_resume.html",{'form':resume_form})

def dashboard(request):
	user = request.user
	applicant = Applicant.objects.filter(user=user).first()
	fields = {
		'First Name' : applicant.user.first_name,
		'Last Name' : applicant.user.last_name,
		'E-mail' : applicant.user.email,
		'Applied Posts': applicant.applied_posts,
		'Uploaded Resume': applicant,
		'Profile Picture': applicant.profile_pic,
		'Phone Number': applicant.phone_number,
		'Key Skills': applicant.key_skills['skills'],

	}
	# print(fields)
	return render(request,"applicant/dashboard.html", {'fields':fields})


def extract_skills(resume_path, applicant_obj):
	data = ResumeParser('media/' + resume_path).get_extracted_data()
	print(data['skills'])
	# applicant_obj = Applicant.objects.get(user = request.user)
	applicant_obj.key_skills = {"skills": data['skills']}
	try :
		applicant_obj.save()
	except Exception as e:
			print("Skill extraction and save error", e )
			# messages.error('Upload not successful')
