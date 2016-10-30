from django.contrib.auth import get_user_model
from pp.models import UserAnswer
from decimal import Decimal
from django.db.models import Q
from pp.models import Question, UserAnswer



def get_match(user_a, user_b):
	q1 = Q(useranswer__user=user_a)
	q2 = Q(useranswer__user=user_b)
	question_set = Question.objects.filter(q1 | q2).distinct()		
	apoints = 0
	bpoints = 0
	atotal = 0
	btotal = 0
	questions_in_common = 0
	for question in question_set:
		try:
			a = UserAnswer.objects.get(user=user_a, question=question)
		except:
			a = None
		try:
			b  = UserAnswer.objects.get(user=user_b, question=question)
		except:
			b = None

		if a and b:
			questions_in_common +=1
			if a.their_answer == b.my_answer:
				bpoints += a.their_points
			btotal += a.their_points
			if b.their_answer == a.my_answer:
				apoints += b.their_points
			atotal += b.their_points
	if questions_in_common > 0:
		adecimal = apoints / Decimal(atotal)
		bdecimal = bpoints / Decimal(btotal)
		print bdecimal, adecimal
		if adecimal == 0:
			adecimal = 0.0000001
		if bdecimal == 0:
			bdecimal= 0.0000001
		match_percentage = (Decimal(adecimal) * Decimal(bdecimal)) ** (1/Decimal(questions_in_common))
		return match_percentage, questions_in_common
	else:
		return 0.0, 0











