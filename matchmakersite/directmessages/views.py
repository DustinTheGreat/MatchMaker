from django.shortcuts import render, get_object_or_404
from .models import DirectMessage
from .forms import ComposeForm
import datetime

# Create your views here.
def inbox(request):
	messages_in_inbox = DirectMessage.objects.filter(reciever=request.user)
	context = {'messages_in_inbox': messages_in_inbox}
	request.session['num_of_messages'] = len(messages_in_inbox)


	return render(request, 'directmessages/inbox.html', context)

def sent(request):
	messages_sent = DirectMessage.objects.filter(sender=request.user)
	context = {'messages_sent':messages_sent}
	return render(request, 'directmessages/sent_inbox.html', context)

def compose(request):
	form = ComposeForm(request.POST or None)
	if form.is_valid():
		send_message = form.save(commit=False)
		send_message.sender= request.user
		send_message.sent  = datetime.datetime.now()
		send_message.save()


	context = {'form':form}
	return render(request, 'directmessages/compose.html', context)

def view_direct_message(request, dm_id):
	message = get_object_or_404(DirectMessage, id=dm_id)
	context = {'message':message}
	if message.reciever == request.user or message.sender == request.user:
		return render(request, 'directmessages/view.html', context)
def reply(request, dm_id ):
	parent_id=dm_id
	parent = get_object_or_404(DirectMessage, id=dm_id)

	form = ComposeForm(request.POST or None)
	if form.is_valid():
		send_message = form.save(commit=False)
		send_message.sender= request.user
		send_message.reciever = parent.sender
		send_message.sent  = datetime.datetime.now()
		send_message.parent = parent
		send_message.save()
		parent.replied = True
		parent.save()



	context = {'form':form}
	return render(request, 'directmessages/compose.html', context)
