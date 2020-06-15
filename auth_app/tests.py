from django.test import TestCase, Client
from django.urls import reverse
import unittest
from django.contrib.auth.models import User

from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By



# Create your tests here.
class TestAuth(TestCase):
	""" Mise en place des tests """
	def setUp(self):
		""" Mise en place des bases de données """
		test_user1 = User.objects.create_user(username="testuser1", password='testtest')
		test_user2 = User.objects.create_user(username="testuser2", password='testtest')

		test_user1.save()
		test_user2.save()

	def test_log_in(self):
		login = self.client.login(username="testuser1", password='testtest')
		response = self.client.get(reverse('login'))
		self.assertEqual(str(response.context['user']), 'testuser1')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'log_in.html')

	def test_log_out(self):
		login = self.client.login(username="testuser2", password='testtest')
		response = self.client.get(reverse('logout'))
		self.assertIsNone(response.context)
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/polls/')


class AccountTestCase(LiveServerTestCase):

	def setUp(self):
		self.selenium = webdriver.Firefox(executable_path='webdriver\\geckodriver.exe')
		super(AccountTestCase, self).setUp()

	def tearDown(self):
		self.selenium.quit()
		super(AccountTestCase, self).tearDown()

	def test_register(self):
		selenium = self.selenium
		#Opening the link we want to test
		selenium.get('http://127.0.0.1:8000/auth_app/signe_it/')
		#find the form element
		username = selenium.find_element_by_id('id_username')
		email = selenium.find_element_by_id('id_email')
		password1 = selenium.find_element_by_id('id_pass_first')
		password2 = selenium.find_element_by_id('id_pass_second')

		submit = selenium.find_element_by_name('register')

		#Fill the form with data
		username.send_keys('TestSelenium')
		email.send_keys('yusuf@qawba.com')
		password1.send_keys('test123456')
		password2.send_keys('test123456')

		#submitting the form
		submit.send_keys(Keys.RETURN)
		print(selenium.current_url)
		selenium.implicitly_wait(10)

		#check the returned result
		self.assertEqual(selenium.find_element_by_css_selector("p#information").get_attribute("innerHTML").splitlines()[0],"Vous avez maintenant un compte sur notre site")

	def test_signeUp(self):
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




