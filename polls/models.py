from django.db import models
from django.contrib.auth.models import User

# Create your models here.
"""class Comptes(models.Model):
	nom = models.CharField(max_length=100)
	prenom = models.CharField(max_length=100)
	mail = models.CharField(max_length=100)
	date_created = models.DateField()
	id_comptes = models.OneToOneField(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.comptes_text"""
