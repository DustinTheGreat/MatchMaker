from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from .utills import get_match
from django.utils import timezone 
import datetime
from decimal import Decimal
# Create your models here.

class MatchQuerySet(models.query.QuerySet):
	def matches(self,user):
		q1 = self.filter(user_a = user)
		q2 = self.filter(user_b = user)
		return (q1 | q2).distinct()


class MatchManager(models.Manager):
	def get_queryset(self):
		return MatchQuerySet(self.model, using=self._db)


	def get_or_create_match(self, user_a=None, user_b=None):
		try:
			obj = self.get(user_a=user_a, user_b=user_b)
		except:
			obj = None
		try:
			obj_2 = self.get(user_a=user_b, user_b=user_a)
		except:
			obj_2 = None
		
		if obj and not obj_2:
			return obj, False
		elif not obj and obj_2:
			return obj_2, False
		else:
			new_instance = self.create(user_a=user_a, user_b=user_b)
			new_instance.do_update()
			##add match percent below
			'''match_decimal, questions_answered = get_match(user_a, user_b)
			new_instance.match_decimal= match_decimal
			new_instance.questions_answered= questions_answered
			new_instance.save()'''
			return new_instance, True
			print "this is made"

	def matches_all(self, user):
		return self.get_queryset().matches(user)


class match(models.Model):
	user_a= models.ForeignKey(settings.AUTH_USER_MODEL, related_name='match_user_a' )
	user_b= models.ForeignKey(settings.AUTH_USER_MODEL, related_name='match_user_b' )
	match_decimal= models.DecimalField(decimal_places=8, max_digits=16, default=0.00)
	questions_answered = models.IntegerField(default=0)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
 
	def __str__(self):
		return "%.2f" %(self.match_decimal)
	objects = MatchManager() # this is a model manager

	

	@property
	def get_percent(self):
		new_decimal = self.match_decimal * Decimal(100)
		return "%.2f" %(new_decimal)






	def do_update(self):
		user_a = self.user_a
		user_b = self.user_b
		match_decimal, questions_answered = get_match(user_a, user_b)
		self.match_decimal = match_decimal
		self.questions_answered = questions_answered
		self.save()


	def check_update(self):
		now  = timezone.now()
		offset = now - datetime.timedelta(hours=12) # 12 hours ago
		if self.updated <= offset or self.match_decimal == 0.0:
			self.do_update()
		else:
			print('already updated')


		#if update is needed


'''

these are model managers!

Match.objects.all()
Match.objects.get()
Match.objects.create()




'''