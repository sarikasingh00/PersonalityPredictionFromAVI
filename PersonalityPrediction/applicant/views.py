from django.shortcuts import render, redirect
from django.contrib import messages
from sklearn import pipeline
from user.models import Applicant
from .forms import ApplicantResumeForm, ApplicantAVIForm
from pyresparser import ResumeParser
import audio_model
import image_model
import avi_features
# from django.shortcuts import HttpResponseRedirect
import datetime
# from datetime import date



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



def avi_upload(request):
	print("in avi upload view")
	applicant_obj = Applicant.objects.get(user = request.user)
	if request.method == 'POST':
		print("in POST")
		avi_file = request.FILES['avi']
		applicant_obj.avi = avi_file
		applicant_obj.avi_upload_date = datetime.date.today().strftime("%Y-%m-%d")
		try :
			applicant_obj.save()
			messages.success(request, 'Video Interview Uploaded!')
			print(applicant_obj.avi.name)
			audio_feature_path, video_feature_path = avi_features.feature_pipeline(applicant_obj.avi.name)
			print(audio_feature_path, video_feature_path)
			print("audio ft extracted, moving to preds")
			print(audio_model.ocean_predict(audio_feature_path))
			print(image_model.ocean_predict(video_feature_path))
		except Exception as e:
			print("Object not saved", e )
			messages.error(request, 'Upload not successful')
	
		return redirect('home')
	
	else:
		if applicant_obj.avi_upload_date is None:
			avi_form = ApplicantAVIForm()
			return render(request,"applicant/upload_avi.html",{'flag': True, 'form':avi_form, 'date': 'Never'})
		else:
			applicant_obj = Applicant.objects.get(user = request.user)
			diff = (datetime.date.today() - applicant_obj.avi_upload_date).days
			if diff>180:
				avi_form = ApplicantAVIForm()
				return render(request,"applicant/upload_avi.html",{'flag': True, 'form':avi_form, 'date': applicant_obj.avi_upload_date.strftime("%Y-%m-%d")})
			else: # change flag to flase later
				avi_form = ApplicantAVIForm() #remove later
				return render(request,"applicant/upload_avi.html",{'flag':True, 'form':avi_form, 'date': applicant_obj.avi_upload_date.strftime("%d-%m-%Y")})


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
		# 'Key Skills': applicant.key_skills['skills'],
		'Video Interview': applicant,
	}
	# 
	if 'skills' in applicant.key_skills:
		fields['Key Skills'] = applicant.key_skills['skills']
	else:
		fields['Key Skills'] = ''
	# print(fields)
	# print(audio_model.ocean_predict())
	return render(request,"applicant/dashboard.html", {'fields':fields, 'profile': applicant.profile_pic.url})


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
