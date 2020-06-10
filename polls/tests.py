from django.test import TestCase, Client
from django.urls import reverse
import unittest
from .models import Produits, Favoris
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
		response = self.client.get('/polls/get_compte/testuser2/')
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/polls/log_in/?next=/polls/get_compte/testuser2/')


	def test_favoris(self):
		login = self.client.login(username="testuser1", password='testtest')
		response = self.client.get(reverse('login'))

		self.assertEqual(str(response.context['user']), 'testuser1')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'log_in.html')

		check_favoris = self.client.get('/polls/favoris/')

		self.assertEqual(len(check_favoris.context['trouve']), 2)

		liste_favoris = check_favoris.context['trouve']

		x = 0
		for favoris in liste_favoris:
			if favoris['index']:
				x += 1

		self.assertEqual(x,0)

		favoris_tbl = Favoris.objects.all()

		for item in favoris_tbl:
			item.aff_index = bool(True)
			item.save()

		response = self.client.get(reverse('login'))

		self.assertEqual(str(response.context['user']), 'testuser1')
		self.assertEqual(response.status_code, 200)
		check_favoris = self.client.get('/polls/favoris/')
		liste_favoris = check_favoris.context['trouve']

		x = 0
		for favoris in liste_favoris:
			if favoris['index']:
				x += 1

		self.assertEqual(x,2)

	def test_search(self):
		terme_search = "nutella"
		response = self.client.post('/polls/resultat/'+terme_search+'/', {'search':terme_search})

		if terme_search == "":
			self.assertEqual(response.status_code, 302)
			self.assertRedirects(response, '/polls/')
		else:
			self.assertEqual(response.status_code, 200)
			if response.context['cherche']['error']:
				self.assertEqual(response.status_code, 200)
			else:
				self.assertNotEqual(len(response.context['trouve']), 0)













