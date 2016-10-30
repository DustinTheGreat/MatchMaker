from django.shortcuts import render, get_object_or_404
from .models import Profile
from django.contrib.auth import get_user_model
from matches.models import match
from django.contrib.auth.decorators import login_required
# Create your views here.
User = get_user_model()



@login_required(login_url='/login/')
def profile_view(request, username):
	user = get_object_or_404(User, username=username)
	profile, created = Profile.objects.get_or_create(user=user)
	Match, match_created = match.objects.get_or_create_match(user_a=request.user, user_b=user)
	context = {'profile':profile, 'Match': Match}
	return render(request, 'profiles/profile.html', context)
