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

from .models import Produits, Vendeurs, Nutriments, Favoris,categories
from .forms import Search, SearchMenu
import requests
import json
import io
import os
import configparser

# Create your views here.
def index(request):
	liste_reponse = []
	form = Search()
	formMenu = SearchMenu()
	favoris = True
	user_current = request.user
	try:
		user_favoris = Favoris.objects.filter(user__exact=user_current.id)
		for favoris_obj in user_favoris:
			aff_index = favoris_obj.aff_index
			if aff_index:
				favoris = False
				id_produit = favoris_obj.produits.id
				favoris_produit = Produits.objects.get(id__exact=id_produit)
				produit = {}
				produit['nom'] =  favoris_produit.generic_name_fr
				produit['image'] = favoris_produit.image_front_url
				produit['url'] = favoris_produit.url_site
				produit['id'] = favoris_produit.id
				produit['index'] = aff_index

				liste_reponse.append(produit)
	except:
		favoris = True

	return render(request, 'index.html',{'form': form,'formMenu':formMenu, 'trouve':liste_reponse, 'error':favoris})


def get_resultat(request, search):
	msg_search = ""
	user_current = request.user
	search_user = search
	if len(search_user) == 0:
		return HttpResponseRedirect('/polls/')
	else:
		answer_search = Produits.objects.filter(generic_name_fr__icontains=search_user)

	if not answer_search.exists():
		liste_reponse = search_categorie(search_user,user_current)
		search_null = False
		dico_answer = {"search":search_user}
		#dico_answer = {'error': True}
		message = "Votre demande ne renvois aucune réponse"
		#return render(request, 'resultat.html', {'cherche':dico_answer,'trouve':liste_reponse, "msg_search":message,'formMenu':SearchMenu()})
	else:
		for answer in answer_search:
			id_cat_test = categories.objects.filter(produit__exact=answer.id)
			if answer.grade :
				nutri_score = answer.grade
				image_produit = answer.image_front_url
				ingredient = answer.ingredients_text_fr
				url_open =answer.url_site
				id_produit = answer._id
				if id_cat_test.exists():
					id_tbl_produit = answer.id
					break
			'''
			else:
				if answer.nova_groups:
					nova = answer.nova_groups
					image_produit = answer.image_front_url
					ingredient = answer.ingredients_text_fr
					url_open =answer.url_site
					nutri_score = ""
					id_tbl_produit = answer.id
					break
			'''
		if len(nutri_score) != 0:
			score = nutri_score
			val_cat_produit = categories.objects.filter(produit__exact=id_tbl_produit)
			list_filter_cat = []
			for id_cat in val_cat_produit:
				list_filter_cat.append(id_cat.id) 
			compare_search = Produits.objects.filter(grade__lt=score).filter(categories__in=list_filter_cat)
		"""else:
			score = nova
			compare_search = Produits.objects.filter(nova_groups__lt=score)"""

		dico_answer = {"score":score, "search":search_user,"image":image_produit,"ingredient":ingredient,'url':url_open}

		if not compare_search.exists():
			search_null = True
		else:
			search_null = False
			liste_reponse = generer_dic_produit(compare_search,user_current)

			
	dico_answer['error'] = search_null
	return render(request, 'resultat.html', {'formMenu':SearchMenu(),'cherche':dico_answer,'trouve':liste_reponse,"msg_search":""})

def search_categorie(answer_utilisateur,user_current):
	search_categorie = categories.objects.filter(nom__icontains=answer_utilisateur)
	x = 0
	liste = []

	if not search_categorie.exists():
		search_categorie = regex_search(answer_utilisateur)

	for categorie in search_categorie:
		search_produit = Produits.objects.filter().filter(categories__id=categorie.id)
		if search_produit.exists():
			if x > 0:
				liste = [i for i in liste_reponse]
				liste_reponse = generer_dic_produit(search_produit,user_current)
				liste_reponse = liste + liste_reponse
				liste = []
			else:
				liste_reponse = generer_dic_produit(search_produit,user_current)

			x += 1
	return liste_reponse

def regex_search(search_user):
	x = 0
	terme = ""
	for caractere in search_user:
		if terme == "":
			terme = caractere

		search_categorie = categories.objects.filter(nom__icontains=terme)
		if search_categorie.exists():
			terme = terme + caractere
			x += 1
		else:
			break
	ss_search_user = search_user[0:x]
	search_categorie = categories.objects.filter(nom__icontains=ss_search_user)
	return search_categorie


def generer_dic_produit(compare_search,user_current):
	produit = {}
	reponse = []
	for compare in compare_search:
		produit = {}
		if compare.brands_tags:
			produit['nom'] =  compare.generic_name_fr
			produit['image'] = compare.image_front_url
			produit['url'] = compare.url_site
			produit['id'] = compare.id

			compare_score = compare.grade
			if compare_score == None:
				nutrilien = "oc_projetHuit/assets/img/nutriscore-NC.png"
			else:
				nutrilien = lien_nutriscore(compare_score)
			produit['url_img_nutri'] = nutrilien
			liste_reponse = generer_liste_reponse(produit,reponse,user_current,compare)
	return liste_reponse

def generer_liste_reponse(produit,liste_reponse,user_current,compare):
	save = True
	try:
		user_favoris = Favoris.objects.filter(user__exact=user_current.id)
		for favoris in user_favoris:
			if favoris.produits.id == compare.id:
				save = False
				break
			else:
				save = True
		produit['favoris'] = save
		liste_reponse.append(produit)
	except:
		produit['favoris'] = save
		liste_reponse.append(produit)
		error = "oui"
	return liste_reponse


def redirect_resultat(request):
	search_user = request.POST['search']
	adresse = request.path
	if adresse.find('resultat'):
		adresse_redirect = '/polls/resultat/' + search_user
	else:
		adresse_redirect = '/polls/save/' + search_user

	return HttpResponseRedirect(adresse_redirect,{'formMenu':SearchMenu(),'search': search_user})

def redirect_404(request, excetpion=None):
	msg = "La page demandée n'a pas été trouvé"
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

	nutrilien = lien_nutriscore(compare_score)
	data_produit['url_img_nutri'] = nutrilien

	return render(request, 'aliments.html',{'formMenu':SearchMenu(),'produit':data_produit})

@login_required(login_url="/auth_app/log_in/")
def save_favoris(request):
	x = 0
	news = ""
	liste_reponse = []
	user_current = request.user
	user_favoris = Favoris.objects.filter(user__exact=user_current.id)
	for favoris in user_favoris:
		aff_index = favoris.aff_index
		id_produit = favoris.produits.id
		favoris_produit = Produits.objects.get(id__exact=id_produit)
		produit = {}
		produit['nom'] =  favoris_produit.generic_name_fr
		produit['image'] = favoris_produit.image_front_url
		produit['url'] = favoris_produit.url_site
		produit['id'] = favoris_produit.id
		produit['ingredient'] = favoris_produit.ingredients_text_fr
		produit['index'] = aff_index
		x += 1
		compare_score = favoris_produit.grade
		nutrilien = lien_nutriscore(compare_score)
		produit['url_img_nutri'] = nutrilien
		liste_reponse.append(produit)
	
	if x == 0:
		info = "Vous n'avez pas encore enregistrer de produit"
	else:
		info = "Vous avez enregistrer " + str(x) + " produits, à tous moment vous pouvez les afficher sur votre page d'accueille pour plus de facilité."
		

	if len(liste_reponse) == 0:
		news = "ok"

	return render(request, 'save_favoris.html',{'formMenu':SearchMenu(),'trouve':liste_reponse, 'info': info,'news':news})

def mise_index(request, id_produit):
	favoris_produit = Favoris.objects.get(produits__exact=id_produit)
	bool_index = favoris_produit.aff_index

	if bool_index:
		favoris_produit.aff_index = False
	else:
		favoris_produit.aff_index = True

	favoris_produit.save()	
	return HttpResponseRedirect('/polls/favoris')

@login_required(login_url="/auth_app/log_in/")
def save(request, id_produit):
	user_current = request.user
	produit = Produits.objects.get(id__exact=id_produit)
	Favoris.objects.create(user=user_current,produits=produit,date_ajout=datetime.today,aff_index=False)
	path_back = request.path
	path_good = path_back.replace("save","aliments")
	info = "Vous avez bien enregistrer ce produit"

	return HttpResponseRedirect(path_good, {'formMenu':SearchMenu(),'msg_save': info})

def lien_nutriscore(nutri_point):
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




	