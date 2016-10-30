from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.core.signals import request_finished
from django.dispatch import receiver
# Create your models here


class Question(models.Model):
	text = models.TextField()
	active = models.BooleanField(default=True)
	draft = models.BooleanField(default=False)
	timstamp =models.DateTimeField(auto_now_add=True, auto_now=False)
	#answers = models.ManyToManyField("Answer")

	def __str__(self):

		return self.text[:10]

#foreignkeys give a relationship between the models

class Answer(models.Model):
	question = models.ForeignKey(Question)
	text = models.CharField(max_length=120)
	draft = models.BooleanField(default=False)
	timstamp =models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):

		return self.text[:10]



LEVELS = (

	('Mandatory', 'Mandatory'),
	('Very Important', 'Very Important'),
	('Somewhat Important',  'Somewhat Important'),
	('Not Important', 'Not Important'),
)	
	
class UserAnswer(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	question= models.ForeignKey(Question)
	my_answer= models.ForeignKey(Answer, related_name='user_answer')
	my_answer_importance=models.CharField(max_length=50, choices=LEVELS)
	their_answer=models.ForeignKey(Answer, null=True, blank=True, related_name='match_answer')
	their_answer_importance=models.CharField(max_length=50, choices=LEVELS)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	my_points=models.IntegerField(default=-1)
	their_points=models.IntegerField(default=-1)
	


	def __str__(self):
		return self.my_answer.text[:10]

#using signals to add values to model after its saved/
def score_importance(importance_level):
	if importance_level == "Mandatory":
		points =300
	elif importance_level == "Very Important":
		points =200
	elif importance_level == "Somewhat Important":
		points =50
	elif importance_level == "Not Important":
		points = 0
	else:
		points = 0
	return points
#reciever function. handles what the signal is sending.
@receiver(pre_save, sender=UserAnswer)
def update_user_answer_score(sender, instance, *args, **kwargs):
	my_points = score_importance(instance.my_answer_importance)
	instance.my_points = my_points
	their_points = score_importance(instance.their_answer_importance)
	instance.their_points = their_points





#@reciever(signal, sender)
'''@receiver(pre_save, sender=UserAnswer)

def update_user_answer_score(sender, instance, *args, **kwargs):

	my_points = score_importance(instance.my_answer_importance)
	instance.my_points = my_points
	their_points = score_importance(instance.their_answer_importance)
	instance.their_points = their_points



'''
















