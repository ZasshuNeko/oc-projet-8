# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Produits(models.Model):
	ingredient = models.CharField(max_length=200)
	url_image_ingredients = models.URLField()
	brands_tags = models.CharField(max_length=200)
	grade = models.CharField(max_length=200,blank=True)
	image_front_url = models.URLField()
	image_nutrition_url = models.URLField()
	nova_groups = models.CharField(max_length=200)
	generic_name_fr = models.CharField(max_length=200)
	url_site = models.URLField()
	ingredients_text_fr = models.CharField(max_length=200)
	_id = models.FloatField()

	def __str__(self):
		return self.brands_tags

class Vendeurs(models.Model):
	produits = models.ForeignKey('Produits', on_delete=models.CASCADE)
	nom = models.CharField(max_length=200)

	def __str__(self):
		return self.nom

class Nutriments(models.Model):
	produits = models.ForeignKey('Produits', on_delete=models.CASCADE)
	nom = models.CharField(max_length=200)
	unite = models.CharField(max_length=10)
	valeur = models.FloatField()

	def __str__(self):
		return self.nom

class Favoris(models.Model):
	'''Création du modèle de base de donnée pour les Favoris'''
	produits = models.ForeignKey('Produits', on_delete=models.CASCADE)
	date_ajout = models.DateField(auto_now_add=True)
	aff_index = models.BooleanField(default=False)

	def __str__(self):
		return self.aff_index
