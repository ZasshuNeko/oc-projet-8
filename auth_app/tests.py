from django.test import TestCase, Client
from django.urls import reverse
import unittest
from django.contrib.auth.models import User 

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


