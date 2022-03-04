from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PersonalityTraits(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE) # username password email first_name last_name
    o = models.FloatField(blank=True)
    c = models.FloatField(blank=True)
    e = models.FloatField(blank=True)
    a = models.FloatField(blank=True)
    n = models.FloatField(blank=True)
