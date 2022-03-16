from email.mime import audio
from django.shortcuts import render, redirect
from django.contrib import messages
from sklearn import pipeline
from .models import PersonalityTraits
from user.models import Applicant
from .forms import ApplicantResumeForm, ApplicantAVIForm
from pyresparser import ResumeParser
import audio_model
import image_model
import avi_features
# from django.shortcuts import HttpResponseRedirect
import datetime
# from datetime import date
import matplotlib.pyplot as plt
from io import StringIO, BytesIO
import numpy as np
import plotly.express as px
import plotly.io as pio
import pandas as pd
from plotly.offline import plot
import plotly.graph_objects as go
from json import dumps


# Create your views here.
def home(request):
	if request.method == 'GET':
		return render(request, "applicant/applicant_home.html")


def resume_upload(request):
	print("in resume upload view")
	if request.method == 'POST':
		print("in POST")
		resume_file = request.FILES['resume']
		applicant_obj = Applicant.objects.get(user=request.user)
		if resume_file.name.endswith('.pdf'):
			applicant_obj.resume = resume_file
			try:
				applicant_obj.save()
				messages.success(request, 'Resume Uploaded!')
				print(applicant_obj.resume.name)
				extract_skills(applicant_obj.resume.name, applicant_obj)
			except Exception as e:
				print("Object not saved", e)
				messages.error(request, 'Upload not successful')
		else:
			messages.error(request, 'You must upload a PDF file')
		return redirect('home')
	else:
		print('in get method')
		resume_form = ApplicantResumeForm()
		return render(request, "applicant/upload_resume.html", {'form': resume_form})


# def return_graph(user):
# 	print("return graph")

# 	if PersonalityTraits.objects.filter(user = user).exists():
# 		traits = PersonalityTraits.objects.get(user=user)
# 		df = pd.DataFrame(dict(
# 			# r=[0.1, 0.5, 0.2, 0.2, 0.3],
# 			r = [traits.o, traits.c, traits.e, traits.a, traits.n],
# 			theta= ['Openness', 'Conscientiousness',  'Extraversion', 'Agreeableness', 'Neuroticism']))
		
# 		fig = px.line_polar(df, r='r', theta='theta', line_close=True, range_r=[0,1], title='Your OCEAN Traits', markers=True)
# 		fig.update_traces(fill='toself')

# 		imgdata = BytesIO()
# 		pio.write_image(fig, imgdata, format='svg')
# 		imgdata.seek(0)

# 		data = imgdata.getvalue()
# 		return data
# 	else:
# 		return None

	
def trait_values(user):
	if PersonalityTraits.objects.filter(user = user).exists():
		traits = PersonalityTraits.objects.get(user=user)
		
		r = [traits.o, traits.c, traits.e, traits.a, traits.n],
		return r
	else:
		return None
	

def avi_upload(request):
	print("in avi upload view")
	applicant_obj = Applicant.objects.get(user = request.user)
	if request.method == 'POST':
		print("in POST")
		avi_file = request.FILES['avi']
		if not avi_file.name.endswith('.mp4'):
			messages.error(request, 'You must upload an MP4 file')
			return redirect('home')
		applicant_obj.avi = avi_file
		applicant_obj.avi_upload_date = datetime.date.today().strftime("%Y-%m-%d")
		try :
			applicant_obj.save()
			messages.success(request, 'Video Interview Uploaded!')
			print(applicant_obj.avi.name)
			audio_feature_path, video_feature_path = avi_features.feature_pipeline(applicant_obj.avi.name)
			print(audio_feature_path, video_feature_path)
			print("audio ft extracted, moving to preds")
			audio_pred = audio_model.ocean_predict(audio_feature_path)[0][0]
			img_pred = image_model.ocean_predict(video_feature_path)
			print(audio_pred)
			print(img_pred)
			pred = (audio_pred+img_pred)/2
			pred = pred.tolist()
			if PersonalityTraits.objects.filter(user = request.user).exists():
				traits = PersonalityTraits.objects.get(user = request.user)
				traits.o = pred[0]
				traits.c = pred[1]
				traits.e = pred[2]
				traits.a = pred[3]
				traits.n = pred[4]
			else:
				traits = PersonalityTraits(user=request.user, o=pred[0], c=pred[1], e=pred[2], a=pred[3], n=pred[4])
			
			traits.save()
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
				return render(request,"applicant/upload_avi.html",{'flag':True, 'form':avi_form, 'date': applicant_obj.avi_upload_date.strftime("%d-%m-%Y"),})


def dashboard(request):
	user = request.user
	applicant = Applicant.objects.filter(user=user).first()
	print(applicant.phone_number)
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
	# return render(request,"applicant/dashboard.html", {'fields':fields, 'profile': applicant.profile_pic.url,  'graph':return_graph(request.user).decode('utf-8'), 'traits': dumps(trait_values(request.user))})
	return render(request,"applicant/dashboard.html", {'fields':fields, 'profile': applicant.profile_pic.url, 'traits': dumps(trait_values(request.user))})


def extract_skills(resume_path, applicant_obj):
	print('in extract skills')
	data = ResumeParser('media/' + resume_path).get_extracted_data()
	print(data['skills'])
	# applicant_obj = Applicant.objects.get(user = request.user)
	applicant_obj.key_skills = {"skills": data['skills']}
	try :
		applicant_obj.save()
	except Exception as e:
			print("Skill extraction and save error", e )
			# messages.error('Upload not successful')
