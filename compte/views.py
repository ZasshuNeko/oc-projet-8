from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.template.loader import *
from django.contrib.postgres.search import SearchQuery
from django.urls import reverse
from django.utils.timezone import datetime
from django.contrib.auth.decorators import login_required

from .forms import Edit,SearchMenu
import requests
import json
import io
import os

# Create your views here.
@login_required(login_url="/auth_app/log_in/")
def get_compte(request, user_name):
	login = request.user.username
	first_name = request.user.first_name
	last_name = request.user.last_name
	email = request.user.email
	password = request.user.password

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

	return render(request, 'compte.html', {'formMenu':SearchMenu(),'data':data_compte})

@login_required(login_url="/auth_app/log_in/")
def edit_compte(request, username):
	user_current = request.user

	default_data = {"last_name":user_current.last_name,"first_name":user_current.first_name,"email":user_current.email}

	form = Edit(default_data)


	return render(request, 'compte_edit.html',{'formMenu':SearchMenu(),'form':form})


@login_required(login_url="/auth_app/log_in/")
def edit_valide(request, username):

	user_current = request.user

	if request.method == 'POST' :
		email = request.POST['email']
		last_name = request.POST['last_name']
		first_name = request.POST['first_name']

		user_current.email = email
		user_current.last_name = last_name
		user_current.first_name = first_name

		user_current.save()

	if user_current.first_name == "" and user_current.last_name == "":
		name = user_current.username
	elif user_current.first_name != "" and user_current.last_name == "":
		name = user_current.first_name
	elif user_current.first_name == "" and user_current.last_name != "":
		name = user_current.last_name
	elif user_current.first_name != "" and user_current.last_name != "":
		name = user_current.first_name + " " + user_current.last_name
	else:
		name = "Incognito"
		
	data_compte = {'email': user_current.email, 'name': name,'formMenu':SearchMenu()}

	return render(request, 'compte.html', data_compte)