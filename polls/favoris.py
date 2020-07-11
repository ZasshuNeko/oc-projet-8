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

class ClassFavoris:

	def bt_see_favoris(user_current):
		x = 0
		news = ""
		liste_reponse = []
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

		return [liste_reponse,info,news]

	def bt_save_favoris(user_current,id_produit,request):
		produit = Produits.objects.get(id__exact=id_produit)
		Favoris.objects.create(
			user=user_current,
			produits=produit,
			date_ajout=datetime.today,
			aff_index=False)
		path_back = request.path
		path_good = path_back.replace("save", "aliments")
		info = "Vous avez bien enregistrer ce produit"

		return [info,path_good]

	def view_index(user_current):
		favoris = True
		liste_reponse = []
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

		return [liste_reponse,favoris]

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