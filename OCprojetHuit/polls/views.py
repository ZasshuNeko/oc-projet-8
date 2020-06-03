#from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.template.loader import *

from .forms import LogIn,SignIt,Search
import requests
import json
import io
import os

# Create your views here.
def index(request):
	form = Search()
	return render(request, 'index.html',{'form': form})

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

def get_compte(request):
	login = request.user.username
	first_name = request.user.first_name
	last_name = request.user.last_name
	email = request.user.email
	password = request.user.password

	#data = {'email': email}
	#form = Compte(data)

	if first_name == "" and last_name == "":
		name = login
	elif first_name != "" and last_name == "":
		name = first_name
	elif first_name == "" and last_name != "":
		name = last_name
	elif first_name != "" and last_name != "":
		name = first_name + " " + last_name
	else:
		name = "Incognito"
	data_compte = {'email': email, 'name': name}

	return render(request, 'compte.html', data_compte)


def get_signeit(request):
	password = False

	if request.method == 'POST' :
		form = SignIt(request.POST)
		username = request.POST['username']
		email = request.POST['email']
		pass_first = request.POST['pass_first']
		pass_second = request.POST['pass_second']

		if pass_first == pass_second:
			password = True
			pass_final = pass_first

		if form.is_valid() and password == True:
			user = User.objects.create_user(username, email, pass_final)
			indication = "Vous avez maintenant un compte sur notre site"
			return HttpResponseRedirect('/polls/',{'news': indication})
	else:
		form = SignIt()

	return render(request, 'signe_it.html', {'form': form})

def get_resultat(request):


	return render(request, 'resultat.html')


def get_aliments(request):
	#url = "https://fr.openfoodfacts.org/categories.json"
	

		

	'''for index, dic in enumerate(f['tags']):
		for cle,valeur in dic.items():
			if cle == "name":
				cle_dico = "produit" + str(index)
				dico[cle_dico] = valeur'''


	return render(request, 'aliments.html')