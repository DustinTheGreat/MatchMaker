from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from matches.models import match
from django.contrib.auth import get_user_model




User = get_user_model()
@login_required(login_url='/login/')
def home(request):
	matches = match.objects.matches_all(request.user)
	context = {'matches':matches}	
	return render(request, 'matchmakersite/home.html', context )
