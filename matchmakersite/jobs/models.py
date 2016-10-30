from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from localflavor.us.models import USStateField

# Create your models here.
User = settings.AUTH_USER_MODEL
class Job(models.Model):
	text = models.TextField(max_length=300)
	flagged = models.ManyToManyField(User,null=True)
	active = models.BooleanField(default=True)
	def __str__(self):
		return self.text


class Location(models.Model):
	text = models.CharField(max_length=500)
	flagged = models.ManyToManyField(User,null=True)
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.text

class Employer(models.Model):
	name = models.CharField(max_length=250)
	location = models.ForeignKey(Location, null=True)
	state = USStateField(null=True)
	
	def __str__(self):
		return self.name