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

from .models import Produits, Vendeurs, Nutriments, Favoris, categories
from .forms import Search, SearchMenu, MultiSelect
import requests
import json
import io
import os
import unicodedata
from .search import ClassSearch
from .favoris import ClassFavoris

# Create your views here.
def index(request):
	''' Génère la vue de l'index
	Generate index view '''
	form = Search()
	formMenu = SearchMenu()
	user_current = request.user

	resultat_class = ClassFavoris.view_index(user_current)
	liste_reponse = resultat_class[0]
	favoris = resultat_class[1] 

	return render(request,
				  'index.html',
				  {'form': form,
				   'formMenu': formMenu,
				   'trouve': liste_reponse,
				   'error': favoris})


def get_resultat(request, search):
	'''Cette vue est appélé lors de la demande d'un utilisateur
	This view is called when a user requests it '''
	msg_search = ""
	user_current = request.user
	search_user = search
	if len(search_user) == 0:
		return HttpResponseRedirect('/polls/')
	else:
		answer_search = Produits.objects.filter(
			generic_name_fr__icontains=search_user)

	resultat_class = ClassSearch.global_search(search_user,user_current,request,answer_search)
	
	dico_answer = resultat_class[0]
	liste_affiche = resultat_class[1]
	dico_other_produit = resultat_class[2]
	form_multi = resultat_class[3]

	return render(request,
				  'resultat.html',
				  {'formMenu': SearchMenu(),
				   'cherche': dico_answer,
				   'trouve': liste_affiche,
				   'multi': dico_other_produit,
				   'form_multi':form_multi,
				   "msg_search": ""})

def get_resultat_id(request):
	''' Appelé quand l'utilisateur utilise la liste déroulante des produits
	répondant à sa recherche initiale
	'''

	if request.method == 'POST':
		id_produit = request.POST['select_produit']
		user_current = request.user

	resultat_class = ClassSearch.select_search(id_produit,user_current)
	
	dico_answer = resultat_class[0]
	liste_affiche = resultat_class[1]
	dico_other_produit = resultat_class[2]
	form_multi = resultat_class[3]
		

	return render(request,
				  'resultat.html',
				  {'formMenu': SearchMenu(),
				   'cherche': dico_answer,
				   'trouve': liste_affiche,
				   'multi': dico_other_produit,
				   'form_multi':form_multi,
				   "msg_search": ""})


def redirect_resultat(request):
	''' Redirige l'utilisateur selon une demande de sauvegardes/résultats
	Redirects the user according to a backup / results request '''
	search_user = request.POST['search']
	adresse = request.path
	if adresse.find('resultat'):
		adresse_redirect = '/polls/resultat/' + search_user
	else:
		adresse_redirect = '/polls/save/' + search_user

	return HttpResponseRedirect(
		adresse_redirect, {
			'formMenu': SearchMenu(), 'search': search_user})


def redirect_404(request, excetpion=None):
	msg = "La page demandée n'a pas été trouvé"
	return redirect('/polls/', {'msg': msg})


def get_aliment(request, id_produit):
	''' Montre une fiche d'un aliment sélectionné
	Show a record of a selected food '''
	data_produit = {}

	produit = Produits.objects.get(id__exact=id_produit)

	data_produit['nom'] = produit.generic_name_fr
	data_produit['image'] = produit.image_front_url
	data_produit['ingredient'] = produit.ingredients_text_fr
	data_produit['url'] = produit.url_site
	data_produit['nutrition'] = produit.image_nutrition_url

	nutriment = Nutriments.objects.filter(produits__exact=id_produit)

	data_produit['nutriment'] = nutriment

	compare_score = produit.grade

	nutrilien = lien_nutriscore(compare_score)
	data_produit['url_img_nutri'] = nutrilien

	return render(
		request, 'aliments.html', {
			'formMenu': SearchMenu(), 'produit': data_produit})


@login_required(login_url="/auth_app/log_in/")
def save_favoris(request):
	''' Permet de ramener les favoris de l'utilisateur
	Returns user favorites '''
	
	user_current = request.user
	resultat_class = ClassFavoris.bt_see_favoris(user_current)
	
	liste_reponse = resultat_class[0]
	info = resultat_class[1]
	news = resultat_class[2]

	return render(request,
				  'save_favoris.html',
				  {'formMenu': SearchMenu(),
				   'trouve': liste_reponse,
				   'info': info,
				   'news': news})


def mise_index(request, id_produit):
	''' Permet d'afficher le bouton pour la mise en index ou le retirer de l'index
	Display the button for indexing or remove it from the index '''
	try:
		favoris_produit = Favoris.objects.get(produits__exact=id_produit)
	except:
		favoris_produit = Favoris.objects.filter(produits__exact=id_produit)[0]
		#print(favoris_produit)
	bool_index = favoris_produit.aff_index

	if bool_index:
		favoris_produit.aff_index = False
	else:
		favoris_produit.aff_index = True

	favoris_produit.save()
	return HttpResponseRedirect('/polls/favoris')


@login_required(login_url="/auth_app/log_in/")
def save(request, id_produit):
	''' Permet de sauvegarder en favoris
	Save to favorites '''
	user_current = request.user
	resultat_class = ClassFavoris.bt_save_favoris(user_current,id_produit,request)
	info = resultat_class[0]
	path_good = resultat_class[1]

	return HttpResponseRedirect(
		path_good, {
			'formMenu': SearchMenu(), 'msg_save': info})


def lien_nutriscore(nutri_point):
	''' Ramène le lien vers l'image de nutriscore
	Brings back the link to the nutriscore image '''
	compare_score = nutri_point

	if int(compare_score) >= -15 and int(compare_score) <= -2:
		lien = "oc_projetHuit/assets/img/nutriscore-A.png"
	elif int(compare_score) >= -1 and int(compare_score) <= 3:
		lien = "oc_projetHuit/assets/img/nutriscore-B.png"
	elif int(compare_score) >= 4 and int(compare_score) <= 11:
		lien = "oc_projetHuit/assets/img/nutriscore-C.png"
	elif int(compare_score) >= 12 and int(compare_score) <= 16:
		lien = "oc_projetHuit/assets/img/nutriscore-D.png"
	elif int(compare_score) >= 17 and int(compare_score) <= 40:
		lien = "oc_projetHuit/assets/img/nutriscore-E.png"

	return lien
