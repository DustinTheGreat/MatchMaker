from django.shortcuts import render, get_object_or_404, redirect
from .models import Question,Answer, UserAnswer
from .forms import UserResponseForm
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from matches.models import match
# Create your views here.


User = get_user_model()
@login_required(login_url='/login/')
def home(request):
	matches  = []
	match_set = match.objects.matches_all(request.user).order_by("-match_decimal")
	for matchy in match_set:
		if matchy.user_a == request.user and matchy.user_b != request.user:
			items_wanted = [matchy.user_b,matchy.get_percent]
			matches.append(items_wanted)
		elif matchy.user_b == request.user and matchy.user_a != request.user:
			items_wanted = [matchy.user_a,matchy.get_percent]
			matches.append(items_wanted)



	context = {'matches':matches}	
	return render(request, 'pp/home.html', context )




def index(request):
 	queryset = Question.objects.all()
 	query = request.GET.get("q")
 	if query:
 		queryset = queryset.filter(text__icontains=query)


 	context = {
 		'queryset': queryset
 	}
 	return render(request, 'pp/index.html', context)





def single(request, id):
	queryset = Question.objects.all()
 	instance = get_object_or_404(Question, id=id)
 	try:
 		user_answer =  UserAnswer.objects.get(user=request.user, question=instance)
 	except UserAnswer.DoesNotExist:
 		user_answer = UserAnswer()
 	except UserAnswer.MultipleObjectReturned:
 		user_answer =  UserAnswer.objects.filter(user=request.user, question=instance)[0]
 	except:

 		user_answer= UserAnswer()



	form = UserResponseForm(request.POST or None)

	if form.is_valid():
		print form.cleaned_data


	#these are just the form inputs! nothing is being saved yet. Im just settings variables 
		question_id = form.cleaned_data.get('question_id')
		answer_id = form.cleaned_data.get('answer_id')
		their_answer_id = form.cleaned_data.get('their_answer_id')
		importance_level = form.cleaned_data.get('importance_level')
		their_importance_level = form.cleaned_data.get('their_importance_level')
		


		question_instance = Question.objects.get(id=question_id)
		answer_instance = Answer.objects.get(id=answer_id)

	#this is settings a varible and saving the info into the database, however it doesnt get saved until they very end when   new_user_answer.save()
		user_answer.user = request.user
		user_answer.question= question_instance
		user_answer.my_answer = answer_instance

		user_answer.my_answer_importance = importance_level
		if their_answer_id != -1:

			their_answer_instance = Answer.objects.get(id=their_answer_id)
			user_answer.their_answer =  their_answer_instance
			user_answer.their_answer_importance = importance_level
		else:
			user_answer.their_answer =  None
			user_answer.their_answer_importance = "Not Important"





		user_answer.save()


		next_q = Question.objects.all().order_by("?").first()
		return redirect("question-single", id= next_q.id)



 	
 	context = {
 		'user_answer':user_answer,
 		'instance':instance,
 		'form': form
 		#'queryset': queryset
 	}
 	return render(request, 'pp/base.html', context)







def question(request):
	form = UserResponseForm(request.POST or None)

	if form.is_valid():
		print form.cleaned_data
		question_id = form.cleaned_data.get('question_id')
		answer_id = form.cleaned_data.get('answer_id')
		question_instance = Question.objects.get(id=question_id)
		answer_instance = Answer.objects.get(id=answer_id)
		print answer_instance.text, question_instance.text
 	queryset = Question.objects.all()
 	instance = queryset[1]
 	context = {
 		'instance':instance,
 		'form': form
 		#'queryset': queryset
 	}
 	return render(request, 'pp/base.html', context)



def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                
                albums = UserAnswer.objects.filter(user=request.user)
                return render(request, 'pp/home.html', {'albums': albums})
            else:
                return render(request, 'pp/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'pp/login.html', {'error_message': 'Invalid login'})
    return render(request, 'pp/login.html')

