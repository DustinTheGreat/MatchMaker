from django import forms
from .models import LEVELS, Answer, Question



#this is to 
class UserResponseForm(forms.Form):
	question_id = forms.IntegerField()
	answer_id = forms.IntegerField() 
	importance_level = forms.ChoiceField(choices=LEVELS)
	their_answer_id = forms.IntegerField()
	their_importance_level = forms.ChoiceField(choices=LEVELS)
	#form validation errors below
	'''def clean_question_id(self):
		question_id = self.cleaned_data.get('question_id')
		try:
			obj  = Question.objects.get(id=question_id)
		except:
			raise forms.ValidationError("there was an error with the answer")
		return question_id



	def clean_answer_id(self):
		answer_id = self.cleaned_data.get('answer_id')
		try:
			obj  = Answer.objects.get(id=anwser_id)
		except:
			raise forms.ValidationError("there was an error with the answer")
		return answer_id

	def clean_their_answer_id(self):
		their_answer_id = self.cleaned_data.get('their_answer_id')
		try:
			obj  = Answer.objects.get(id=their_anwser_id)
		except:
			raise forms.ValidationError("there was an error with the answer you provided for them")
		return their_answer_id'''

	
	
