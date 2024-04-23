from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from kanectapp.models import *
from django.contrib.auth import login as auth_login
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def home(request):
	return render(request, 'home.html')

def signup(request):
	if request.method == 'POST':
		post_data = request.POST
		get_user_data = User.objects.filter(username = post_data['username'])
		if get_user_data:
			return render(request, 'signup.html', {'error':'username already exists'})
		else:
			user = User.objects.create(username = post_data['username'], password = post_data['password'])
			user.set_password(post_data['password'])
			user.save()
			return render(request, 'login.html')
		
	return render(request, 'signup.html')

def login(request):
	if request.method == 'POST':
		post_data = request.POST
		print(post_data)
		get_user_data = User.objects.filter(username = post_data['username'])
		if get_user_data:
			for user in get_user_data:
				if user.check_password(post_data['password']):
					auth_login(request, user)
					return redirect('/chats/')
				else:
					return render(request, 'login.html', {'error':'username or password is incorrect'})
		else:
			return render(request, 'login.html', {'error':'username or password is incorrect'})

	return render(request, 'login.html')

def logout(request):

	return redirect('/login/')


def chats(request):
	print(request.user, 'came in request')
	all_users = list(User.objects.exclude(username = request.user).values_list('username', flat = True))
	all_users = list(filter(None, all_users))
	print(all_users)
	return render(request, 'chats.html', {'users':all_users})

@csrf_exempt
def user_chat(request):
	print(request.user)
	post_data = request.POST
	print(post_data)
	messages = Chats.objects.filter(username = request.user, chatted_with = post_data['username'])

	if not messages:
		messages = {}
		messages['sent_messages'] = ''
		data = {'user':post_data['username'], 'messages':''}

	else:
		serialized_messages = list(messages.values('sent_messages'))
		print(serialized_messages)
		data = {'user':post_data['username'], 'messages':serialized_messages[0]['sent_messages']}
	return JsonResponse(data)

def send_message(request):
	post_data = request.POST
	print(request.user, 'request user')
	print(post_data, 'send_message post data')
	message_dict = {'message':post_data['message'], 'time':datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'sent_by':str(request.user)}
	messages = Chats.objects
	if not messages.filter(username = request.user, chatted_with = post_data['username']):
		messages.create(username = request.user, chatted_with = post_data['username'], sent_messages = [message_dict], time = datetime.now())
		messages.create(username = post_data['username'], chatted_with = request.user, sent_messages = [message_dict], time = datetime.now())
	elif not messages.filter(username = request.user, chatted_with = post_data['username']).values('sent_messages'):
		messages.create(username = request.user, chatted_with = post_data['username'], sent_messages = [message_dict], time = datetime.now())
		messages.create(username = post_data['username'], chatted_with = request.user, sent_messages = [message_dict], time = datetime.now())
	else:
		messages = Chats.objects.filter(username = request.user, chatted_with = post_data['username']).first()
		print(messages)
		sent_messages = messages.sent_messages
		print(sent_messages)
		sent_messages.append(message_dict)
		messages.sent_messages = sent_messages
		messages.save()

		messages = Chats.objects.filter(username = post_data['username'], chatted_with = request.user).first()
		print(messages)
		sent_messages = messages.sent_messages
		print(sent_messages)
		sent_messages.append(message_dict)
		messages.sent_messages = sent_messages
		messages.save()

	messages = Chats.objects.filter(username = request.user, chatted_with = post_data['username'])
	serialized_messages = list(messages.values('sent_messages'))
	print(serialized_messages)
	data = {'user':post_data['username'], 'messages':serialized_messages[0]['sent_messages']}
	return JsonResponse(data)