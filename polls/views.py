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


# Create your views here.
def index(request):
	''' Génère la vue de l'index
	Generate index view '''
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
				produit['nom'] = favoris_produit.generic_name_fr
				produit['image'] = favoris_produit.image_front_url
				produit['url'] = favoris_produit.url_site
				produit['id'] = favoris_produit.id
				produit['index'] = aff_index

				liste_reponse.append(produit)
	except BaseException:
		favoris = True

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

	if not answer_search.exists():
		liste_render = search_categorie(search_user, user_current, request)
		liste_results = liste_render[0]
		id_select = liste_render[2]
		if len(liste_results) == 0:
			search_null = True
			dico_answer = {"search": search_user}
			liste_affiche = []
			results_view = multi_answer(liste_render[1],dico_answer,id_select)
			dico_other_produit = results_view[0]
			dico_answer = results_view[1]
		else:
			search_null = False
			dico_answer = liste_results[1]
			liste_affiche = liste_results[0]
			results_view = multi_answer(liste_render[1],dico_answer,id_select)
			dico_other_produit = results_view[0]
			dico_answer = results_view[1]
	else:
		for answer in answer_search:
			produit_caracteristique = selection_produit(answer)
			if len(produit_caracteristique) == 9:
				break

		liste_render = selection_reponse(produit_caracteristique,search_user,user_current)
		search_null = liste_render[2]
		dico_answer = liste_render[1]
		liste_affiche = liste_render[0]
		results_view = multi_answer(answer_search,dico_answer,produit_caracteristique[8])
		dico_other_produit = results_view[0]
		dico_answer = results_view[1]

	form_multi = MultiSelect()
	liste_tuple = []
	for select in results_view[0]:
		id_produit = str(select.get('id'))
		nom_produit = select.get('nom') + '[' + select.get('qte') + ']'
		tuple_produit = (id_produit, nom_produit)
		liste_tuple.append(tuple_produit)

	form_multi.fields['select_produit'].choices = liste_tuple
	form_multi.fields['select_produit'].initial = [1]

	dico_answer['error'] = search_null

	return render(request,
				  'resultat.html',
				  {'formMenu': SearchMenu(),
				   'cherche': dico_answer,
				   'trouve': liste_affiche,
				   'multi': dico_other_produit,
				   'form_multi':form_multi,
				   "msg_search": ""})

def get_resultat_id(request):

	if request.method == 'POST':
		id_produit = request.POST['select_produit']

		user_current = request.user
		id_prop = Produits.objects.filter(
				id__exact=id_produit).values()
		id_search = Produits.objects.filter(
				id__exact=id_produit)
		for produit in id_search:
			produit_caracteristique = selection_produit(produit)
		search_user = id_prop[0].get('generic_name_fr')
		liste_render = selection_reponse(produit_caracteristique,search_user,user_current)
		search_null = liste_render[2]
		dico_answer = liste_render[1]
		liste_affiche = liste_render[0]
		answer_search = Produits.objects.filter(
				generic_name_fr__icontains=search_user)
		results_view = multi_answer(answer_search,dico_answer,produit_caracteristique[8])
		dico_other_produit = results_view[0]
		dico_answer = results_view[1]


	form_multi = MultiSelect()
	liste_tuple = []
	for select in results_view[0]:
		id_produit = str(select.get('id'))
		nom_produit = select.get('nom') + '[' + select.get('qte') + ']'
		tuple_produit = (id_produit, nom_produit)
		liste_tuple.append(tuple_produit)

	form_multi.fields['select_produit'].choices = liste_tuple
	form_multi.fields['select_produit'].initial = [1]

	dico_answer['error'] = search_null

	return render(request,
				  'resultat.html',
				  {'formMenu': SearchMenu(),
				   'cherche': dico_answer,
				   'trouve': liste_affiche,
				   'multi': dico_other_produit,
				   'form_multi':form_multi,
				   "msg_search": ""})


def multi_answer(answer_search,dico_answer,id_select):
	''' Ce module gère en cas de réponses multiple
	'''
	if len(answer_search) > 1:
		dico_other_produit = other_produit(answer_search,id_select)
		dico_answer['multi'] = True
	else:
		dico_answer['multi'] = False
		dico_other_produit = []

	return [dico_other_produit,dico_answer]


def other_produit(produits,id_select):
	''' Selection des produits multiples
	'''
	liste_produit = []
	for produit in produits:
		if produit.id != id_select:
			nom = produit.generic_name_fr
			id_produit = produit.id
			qte_produit = produit.nova_groups
			dico = {'nom':nom,
			'id': id_produit,
			'qte': qte_produit}
			liste_produit.append(dico)
	return liste_produit



def selection_reponse(caract_prod,search_user,user_current):
	''' Ramène les propriété du produit à comparé, et la liste des produits 
	trouvé dut à cette comparaison
	'''

	nutri_score = caract_prod[0]
	image_produit = caract_prod[1]
	ingredient = caract_prod[2]
	url_open = caract_prod[3]
	id_produit = caract_prod[4]
	nom_produit = caract_prod[5]
	image_nutrition = caract_prod[6]
	qte_produit = caract_prod[7]
	id_tbl_produit = caract_prod[8]


	if len(nutri_score) != 0:
		score = nutri_score
		nutrilien = lien_nutriscore(score)
		val_cat_produit = categories.objects.filter(
			produit__exact=id_tbl_produit)
		list_filter_cat = []
		for id_cat in val_cat_produit:
			list_filter_cat.append(id_cat.id)
		compare_search = Produits.objects.filter(grade__lt=score).filter(
			categories__in=list_filter_cat).order_by('grade')
		if not compare_search.exists():
			compare_search = Produits.objects.filter(grade__lte=score).filter(
				categories__in=list_filter_cat).order_by('grade')

	dico_answer = {
		"score": score,
		"search": search_user,
		"image": image_produit,
		"ingredient": ingredient,
		'url': url_open,
		'nom': nom_produit,
		'nutrilien': nutrilien,
		'img_nutri': image_nutrition,
		'qte': qte_produit}


	if not compare_search.exists():
		search_null = True
		liste_reponse = []
	else:
		search_null = False
		liste_reponse = generer_dic_produit(compare_search, user_current)

	return [liste_reponse,dico_answer,search_null]



def selection_produit(answer):
	''' Ramène les propriétées d'un produit sélectionner
	'''
	id_cat_test = categories.objects.filter(produit__exact=answer.id)
	if answer.grade:
		nutri_score = answer.grade
		image_produit = answer.image_front_url
		ingredient = answer.ingredients_text_fr
		url_open = answer.url_site
		id_produit = answer._id
		nom_produit = answer.generic_name_fr
		image_nutrition = answer.image_nutrition_url
		qte_produit = answer.nova_groups
		if id_cat_test.exists():
			id_tbl_produit = answer.id

	return [nutri_score,image_produit,ingredient,url_open,id_produit,nom_produit,image_nutrition,qte_produit,id_tbl_produit]

def search_categorie(answer_utilisateur, user_current, request):
	''' Si le produit n'est pas trouvé dans la base produit, 
	on lui demande de chercher dans la base catégories.
	If the product is not found in the product database,
	it is asked to search in the categories database '''
	answer_no_accent = "".join((c for c in unicodedata.normalize(
		'NFD', answer_utilisateur) if unicodedata.category(c) != 'Mn'))
	search_categorie = categories.objects.filter(
		nom_iaccents__icontains=answer_no_accent)
	x = 0
	liste = []

	if search_categorie.exists():
		search_produit = Produits.objects.filter().filter(categories__id=search_categorie[0].id)
		for answer in search_produit:
			produit_caracteristique = selection_produit(answer)
			if len(produit_caracteristique) == 9:
				break

		id_produit = produit_caracteristique[8]
		liste_render = selection_reponse(produit_caracteristique,answer_utilisateur, user_current)
		all_produit = Produits.objects.filter().filter(categories__in=search_categorie)

	else:
		liste_render = []
		all_produit = []
		id_produit = []

	return [liste_render,all_produit,id_produit]


def generer_dic_produit(compare_search, user_current):
	''' Créer une réponse avec les produits demandés par l'utilisateur
	Create a response with the products requested by the user '''
	produit = {}
	reponse = []
	for compare in compare_search:
		produit = {}
		if compare.brands_tags:
			produit['nom'] = compare.generic_name_fr
			produit['image'] = compare.image_front_url
			produit['url'] = compare.url_site
			produit['id'] = compare.id

			compare_score = compare.grade
			if compare_score is None:
				nutrilien = "oc_projetHuit/assets/img/nutriscore-NC.png"
			else:
				nutrilien = lien_nutriscore(compare_score)
			produit['url_img_nutri'] = nutrilien
			liste_reponse = generer_liste_reponse(
				produit, reponse, user_current, compare)
	return liste_reponse


def generer_liste_reponse(produit, liste_reponse, user_current, compare):
	''' vérifie si un produit trouvé n'est pas déjà enregistré dans les favoris
	checks if a product found is not already saved in favorites '''
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
	except BaseException:
		produit['favoris'] = save
		liste_reponse.append(produit)
		error = "oui"
	return liste_reponse


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
	x = 0
	news = ""
	liste_reponse = []
	user_current = request.user
	user_favoris = Favoris.objects.filter(user__exact=user_current.id)
	for favoris in user_favoris:
		aff_index = favoris.aff_index
		id_produit = favoris.produits.id
		favoris_produit = Produits.objects.get(
			id__exact=id_produit)
		produit = {}
		produit['nom'] = favoris_produit.generic_name_fr
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
		info = "Vous avez enregistrer " + \
			str(x) + " produits, à tous moment vous pouvez les afficher sur votre page d'accueille pour plus de facilité."

	if len(liste_reponse) == 0:
		news = "ok"

	return render(request,
				  'save_favoris.html',
				  {'formMenu': SearchMenu(),
				   'trouve': liste_reponse,
				   'info': info,
				   'news': news})


def mise_index(request, id_produit):
	''' Permet d'afficher le bouton pour la mise en index ou le retirer de l'index
	Display the button for indexing or remove it from the index '''
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
	''' Permet de sauvegarder en favoris
	Save to favorites '''
	user_current = request.user
	produit = Produits.objects.get(id__exact=id_produit)
	Favoris.objects.create(
		user=user_current,
		produits=produit,
		date_ajout=datetime.today,
		aff_index=False)
	path_back = request.path
	path_good = path_back.replace("save", "aliments")
	info = "Vous avez bien enregistrer ce produit"

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
