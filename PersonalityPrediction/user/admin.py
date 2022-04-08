import imp
from django.contrib import admin
from user.models import Applicant,Recruiter
from applicant.models import PersonalityTraits
# Register your models here.
admin.site.register(Applicant)
admin.site.register(Recruiter)
admin.site.register(PersonalityTraits)
