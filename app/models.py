# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Produits(models.Model):
    ingredient = models.CharField(max_length=5000)
    url_image_ingredients = models.URLField(max_length=5000)
    brands_tags = models.CharField(max_length=1000)
    grade = models.CharField(max_length=800, blank=True, null=True)
    image_front_url = models.URLField(max_length=5000)
    image_nutrition_url = models.URLField(max_length=5000)
    nova_groups = models.CharField(max_length=800, null=True)
    generic_name_fr = models.CharField(max_length=5000)
    url_site = models.URLField(max_length=5000)
    ingredients_text_fr = models.CharField(max_length=5000)
    _id = models.FloatField()

    def __str__(self):
        return self.brands_tags


class categories(models.Model):
    nom = models.CharField(max_length=5000)
    nom_iaccents = models.CharField(max_length=5000)
    produit = models.ManyToManyField(Produits)


class Vendeurs(models.Model):
    produits = models.ForeignKey('Produits', on_delete=models.CASCADE)
    nom = models.CharField(max_length=600)

    def __str__(self):
        return self.nom


class Nutriments(models.Model):
    produits = models.ForeignKey('Produits', on_delete=models.CASCADE)
    nom = models.CharField(max_length=900)
    unite = models.CharField(max_length=10)
    valeur = models.FloatField()

    def __str__(self):
        return self.nom


class Favoris(models.Model):
    '''Création du modèle de base de donnée pour les Favoris'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produits = models.ForeignKey('Produits', on_delete=models.CASCADE)
    date_ajout = models.DateField(auto_now_add=True)
    aff_index = models.BooleanField(default=False)

    def __str__(self):
        return self.aff_index
