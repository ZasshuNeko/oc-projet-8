#from django.shortcuts import render
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

from .models import Produits, Vendeurs, Nutriments, Favoris
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

def get_resultat(request, search):
	user_current = request.user
	liste_reponse = []
	#form = Search(request.POST)
	#search_user = request.POST['search']
	search_user = search
	if len(search_user) == 0:
		return HttpResponseRedirect('/polls/')
	else:
		answer_search = Produits.objects.filter(brands_tags__contains=search_user)

	if not answer_search.exists():
		message = "Votre demande ne renvois aucune réponse"
		return HttpResponseRedirect('/polls/',{'msg_search': message})
	else:
		for answer in answer_search:

			if answer.grade:
				nutri_score = answer.grade
				image_produit = answer.image_front_url
				ingredient = answer.ingredients_text_fr
				url_open =answer.url_site
				id_produit = answer._id
				break
			else:
				if answer.nova_groups:
					nova = answer.nova_groups
					image_produit = answer.image_front_url
					ingredient = answer.ingredients_text_fr
					url_open =answer.url_site
					nutri_score = ""
					break

		if len(nutri_score) != 0:
			score = nutri_score
			compare_search = Produits.objects.filter(grade__lt=score)
		else:
			score = nova
			compare_search = Produits.objects.filter(nova_groups__lt=score)

		dico_answer = {"score":score, "search":search_user,"image":image_produit,"ingredient":ingredient,'url':url_open}

		if not compare_search.exists():
			search_null = True
		else:
			search_null = False

			produit = {}
			for compare in compare_search:
				produit = {}
				if compare.brands_tags:
					produit['nom'] =  compare.generic_name_fr
					produit['image'] = compare.image_front_url
					#produit['ingredient'] = compare.ingredients_text_fr
					produit['url'] = compare.url_site
					#produit['nutrition'] = compare.image_nutrition_url
					produit['id'] = compare.id

					#nutriment = Nutriments.objects.filter(produits__exact=compare.id)

					#produit['nutriment'] = nutriment

					compare_score = compare.grade

					if int(compare_score) >= -15 and int(compare_score) <= -2:
						produit['url_img_nutri'] = "oc_projetHuit/assets/img/nutriscore-A.png"
					elif int(compare_score) >= -1 and int(compare_score) <= 3:
						produit['url_img_nutri'] = "oc_projetHuit/assets/img/nutriscore-B.png"
					elif int(compare_score) >= 4 and int(compare_score) <= 11:
						produit['url_img_nutri'] = "oc_projetHuit/assets/img/nutriscore-C.png"
					elif int(compare_score) >= 12 and int(compare_score) <= 16:
						produit['url_img_nutri'] = "oc_projetHuit/assets/img/nutriscore-D.png"
					elif int(compare_score) >= 17 and int(compare_score) <= 40:
						produit['url_img_nutri'] = "oc_projetHuit/assets/img/nutriscore-E.png"

					save = True
					user_favoris = Favoris.objects.filter(user__exact=user_current.id)
					for favoris in user_favoris:
						if favoris.produits.id == compare.id:
							save = False
							break
						else:
							save = True

					produit['favoris'] = save
					liste_reponse.append(produit)

	dico_answer['error'] = search_null
	#liste_reponse.append(dico_answer)
	return render(request, 'resultat.html', {'cherche':dico_answer,'trouve':liste_reponse})

def redirect_resultat(request):
	search_user = request.POST['search']
	adresse = request.path
	if adresse.find('resultat'):
		adresse_redirect = '/polls/resultat/' + search_user
	else:
		adresse_redirect = '/polls/save/' + search_user

	return HttpResponseRedirect(adresse_redirect,{'search': search_user})

def redirect_404(request, excetpion=None):
	msg = "La page demandée n'a pas été trouvé"
	#return HttpResponseRedirect('/polls/',{'msg': msg})
	return redirect('/polls/', {'msg': msg})


def get_aliment(request, id_produit):
	data_produit = {}

	produit = Produits.objects.get(id__exact=id_produit)

	data_produit['nom'] =  produit.generic_name_fr
	data_produit['image'] = produit.image_front_url
	data_produit['ingredient'] = produit.ingredients_text_fr
	data_produit['url'] = produit.url_site
	data_produit['nutrition'] = produit.image_nutrition_url

	nutriment = Nutriments.objects.filter(produits__exact=id_produit)

	data_produit['nutriment'] = nutriment

	compare_score = produit.grade

	if int(compare_score) >= -15 and int(compare_score) <= -2:
		data_produit['url_img_nutri'] = "oc_projetHuit/assets/img/nutriscore-A.png"
	elif int(compare_score) >= -1 and int(compare_score) <= 3:
		data_produit['url_img_nutri'] = "oc_projetHuit/assets/img/nutriscore-B.png"
	elif int(compare_score) >= 4 and int(compare_score) <= 11:
		data_produit['url_img_nutri'] = "oc_projetHuit/assets/img/nutriscore-C.png"
	elif int(compare_score) >= 12 and int(compare_score) <= 16:
		data_produit['url_img_nutri'] = "oc_projetHuit/assets/img/nutriscore-D.png"
	elif int(compare_score) >= 17 and int(compare_score) <= 40:
		data_produit['url_img_nutri'] = "oc_projetHuit/assets/img/nutriscore-E.png"

	return render(request, 'aliments.html',{'produit':data_produit})

@login_required(login_url="log_in/")
def save(request, id_produit):
	user_current = request.user
	produit = Produits.objects.get(id__exact=id_produit)
	Favoris.objects.create(user=user_current,produits=produit,date_ajout=datetime.today,aff_index=False)
	path_back = request.path
	path_good = path_back.replace("save","aliments")
	info = "Vous avez bien enregistrer ce produit"

	return HttpResponseRedirect(path_good, {'msg_save': info})



	