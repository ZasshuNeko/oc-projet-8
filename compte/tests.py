from django.test import TestCase, Client
from django.urls import reverse
import unittest
from polls.models import Produits, Favoris
from django.contrib.auth.models import User

from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Create your tests here.
class TestApp(TestCase):
	""" Mise en place des tests """
	def setUp(self):
		""" Mise en place des bases de données """
		test_user1 = User.objects.create_user(username="testuser1", password='testtest', email="test@test.com")
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

	def test_compte(self):
		login = self.client.login(username="testuser1", password='testtest')
		response = self.client.get(reverse('login'))

		self.assertEqual(str(response.context['user']), 'testuser1')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'log_in.html')

		test_edit = self.client.get('/compte/get_compte/' + str(response.context['user']) +  '/')
		self.assertEqual(test_edit.status_code, 200)
		self.assertTemplateUsed(test_edit, 'compte.html')
		self.assertEqual(str(test_edit.context['data']['name']),str(response.context['user']) )

	def test_compteedit(self):
		login = self.client.login(username="testuser1", password='testtest')
		response = self.client.get(reverse('login'))

		self.assertEqual(str(response.context['user']), 'testuser1')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'log_in.html')

		test_edit = self.client.get('/compte/get_compte/' + str(response.context['user']) +  '/edit/')
		self.assertEqual(test_edit.status_code, 200)
		self.assertTemplateUsed(test_edit, 'compte_edit.html')

	def test_change_info(self):
		login = self.client.login(username="testuser1", password='testtest')
		response = self.client.get(reverse('login'))

		self.assertEqual(str(response.context['user']), 'testuser1')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'log_in.html')

		default_data = {"last_name":"TestDjango","first_name":"TestDjangoFirst","email":"Test@test.test"}

		test_edit = self.client.post('/compte/get_compte/' + str(response.context['user']) +  '/valide/',default_data)
		self.assertEqual(test_edit.status_code, 200)
		self.assertTemplateUsed(test_edit, 'compte.html')

		test_edit = self.client.get('/compte/get_compte/' + str(response.context['user']) +  '/')
		self.assertEqual(test_edit.status_code, 200)
		self.assertEqual(str(test_edit.context['data']['name']),"TestDjangoFirst TestDjango" )


class AccountTestCase(LiveServerTestCase):

	def setUp(self):
		self.selenium = webdriver.Firefox(executable_path='webdriver\\geckodriver.exe')
		super(AccountTestCase, self).setUp()

	def tearDown(self):
		self.selenium.quit()
		super(AccountTestCase, self).tearDown()

	def test_editcompte(self):
		selenium = self.selenium
		#Opening the link we want to test
		selenium.get('http://127.0.0.1:8000/auth_app/log_in/')
		#find the form element
		username = selenium.find_element_by_id('id_log_id')
		password = selenium.find_element_by_id('id_pwd')

		submit = selenium.find_element_by_name('login')

		#Fill the form with data
		username.send_keys('TestSelenium')
		password.send_keys('test123456')

		#submitting the form
		submit.send_keys(Keys.RETURN)
		selenium.implicitly_wait(10)
		name_index = "Bonjour TestSelenium"
		#check the returned result
		self.assertEqual(selenium.find_element_by_css_selector("h1#info_login").get_attribute("innerHTML").splitlines()[0],name_index)

		selenium.get('http://127.0.0.1:8000/compte/get_compte/TestSelenium/edit/')

		first_name = selenium.find_element_by_id('id_first_name')
		last_name = selenium.find_element_by_id('id_last_name')

		first_name.send_keys('')
		last_name.send_keys('')

		first_name.send_keys('TestSelenium')
		last_name.send_keys('Django_test')		

		submit = selenium.find_element_by_name('edit_compte')

		submit.send_keys(Keys.RETURN)
		selenium.implicitly_wait(10)

		first_name = selenium.find_element_by_id('id_first_name')
		last_name = selenium.find_element_by_id('id_last_name')

		print(selenium.find_element_by_id("first").get_attribute("value"))

		self.assertEqual(selenium.find_element_by_id("first").get_attribute("value"), "TestSelenium")
		self.assertEqual(selenium.find_element_by_id("last").get_attribute("value"), "Django_test")








