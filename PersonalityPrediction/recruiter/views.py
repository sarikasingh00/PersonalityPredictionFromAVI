import imp
import re
from django.shortcuts import render

from applicant.models import PersonalityTraits
from user.models import Applicant
from django.contrib.auth.models import User
from applicant.views import trait_values
from json import dumps

# Create your views here.
def dashboard(request):
    print("Recruiter Dahsboard")
    results = None

    if request.method == 'GET':
        # all_applicants = Applicant.objects.all()
        all_applicants = PersonalityTraits.objects.all()
        applicant_objs = []
        for applicant in all_applicants:
            user = applicant.user
            applicant_obj = Applicant.objects.get(user=user)
            applicant_objs += [applicant_obj]
        return render(request,"recruiter/recruiter_home.html", {'applicants': zip(all_applicants, applicant_objs)})
    else:
        if 'O' in request.POST:
            print('in O search')
            o = request.POST['O']
            c = request.POST['C']
            e = request.POST['E']
            a = request.POST['A']
            n = request.POST['N']
            personality_obj = PersonalityTraits.objects.filter(o__gte=float(o), c__gte=float(c), e__gte=float(e), a__gte=float(a), n__gte=float(n))
            applicant_objs = []
            for applicant in personality_obj:
                user = applicant.user
                applicant_obj = Applicant.objects.get(user=user)
                applicant_objs += [applicant_obj]
       
        else:
            if ' ' in request.POST['Search']:
                first_name, last_name = request.POST['Search'].split(' ')
            else:
                first_name = request.POST['Search']
                last_name = ''
            user_results = User.objects.filter(first_name__icontains=first_name, last_name__icontains=last_name)
            print(user_results)
            personality_obj = []
            applicant_objs = []
            for user in user_results:
                print(user)
                if PersonalityTraits.objects.filter(user=user).exists():
                    personality_obj += [PersonalityTraits.objects.get(user=user)]
                    applicant_objs += [Applicant.objects.get(user=user)]

    return render(request,"recruiter/recruiter_home.html", {'applicants': zip(personality_obj, applicant_objs)})


def applicant_profile(request, username):
    print(username)
    user_obj = User.objects.get(username=username)
    applicant = Applicant.objects.get(user=user_obj)
    personality_obj =  PersonalityTraits.objects.get(user=user_obj)
    fields = {
		'First Name' : applicant.user.first_name,
		'Last Name' : applicant.user.last_name,
		'E-mail' : applicant.user.email,
		'Applied Posts': applicant.applied_posts,
		'Uploaded Resume': applicant.resume,
		'Profile Picture': applicant.profile_pic,
		'Phone Number': applicant.phone_number,
		# 'Key Skills': applicant.key_skills['skills'],
		'Video Interview': applicant.avi,
	}
    if 'skills' in applicant.key_skills:
        fields['Key Skills'] = ', '.join(applicant.key_skills['skills'])
    else:
        fields['Key Skills'] = ''
    
    return render(request,"recruiter/applicant_profile.html", {'applicant': applicant, 'traits': dumps(trait_values(user_obj)), 'fields': fields})