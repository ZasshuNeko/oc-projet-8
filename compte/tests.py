from django.test import TestCase, Client
from django.urls import reverse
import unittest
from polls.models import Produits, Favoris
from django.contrib.auth.models import User 

# Create your tests here.
class TestApp(TestCase):
	""" Mise en place des tests """
	def setUp(self):
		""" Mise en place des bases de données """
		test_user1 = User.objects.create_user(username="testuser1", password='testtest')
		test_user2 = User.objects.create_user(username="testuser2", password='testtest')

		test_user1.save()
		test_user2.save()

		id_produit1 = Produits.objects.get(pk=1)
		id_produit2 = Produits.objects.get(pk=2)

		test_favoris = Favoris.objects.create(user=test_user1,produits=id_produit1,date_ajout="08/06/2020",aff_index=False)
		test_favoris.save()
		test_favoris = Favoris.objects.create(user=test_user2,produits=id_produit1,date_ajout="08/06/2020",aff_index=False)
		test_favoris.save()
		test_favoris = Favoris.objects.create(user=test_user2,produits=id_produit2,date_ajout="08/06/2020",aff_index=False)
		test_favoris.save()
		test_favoris = Favoris.objects.create(user=test_user1,produits=id_produit1,date_ajout="08/06/2020",aff_index=False)
		test_favoris.save()

	def test_not_log(self):
		response = self.client.get('/compte/get_compte/testuser2/')
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/auth_app/log_in/?next=/compte/get_compte/testuser2/')




