#from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.template.loader import *

from .forms import LogIn,SignIt


# Create your views here.
def index(request):
	return render(request, 'index.html')

def log_out(request):
	logout(request)
	return redirect('/polls/', {'news':"Vous êtes maintenant déconnecté"})

def get_login(request, user=''):

	if request.method == 'POST' :
		form = LogIn(request.POST)
		username = request.POST['log_id']
		password = request.POST['pwd']
		user = authenticate(request, username=username, password=password)
		if form.is_valid():
			if user is not None:
				login(request, user)
				msg = "Vous êtes maintenant connecté en tant que " + username
				data = {'msg': msg, 'user': username}
				user = username
				return HttpResponseRedirect("/polls/",{'user': username})
	else:
		form = LogIn()

	return render(request, 'log_in.html', {'form': form})


def get_signeit(request):

	if request.method == 'POST' :
		form = SignIt(request.POST)
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['pass_first']

		if form.is_valid() and password == True:
			print(password)
			#user = User.objects.create_user(surname)
			#return HttpResponseRedirect('%s%s' % (request.path, user),{'user': username})
	else:
		form = SignIt()

	return render(request, 'signe_it.html', {'form': form})
