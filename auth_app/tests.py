from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# Create your tests here.
class TestAuth(TestCase):
    """ Mise en place des tests """

    def setUp(self):
        """ Mise en place des bases de données """
        test_user1 = User.objects.create_user(
            username="testuser1", password='testtest')
        test_user2 = User.objects.create_user(
            username="testuser2", password='testtest')

        test_user1.save()
        test_user2.save()

    def test_log_in(self):
        ''' Test de la connexion
        Connection test '''
        default_data = {"log_id": "testuser1", "pwd": "testtest"}
        test_login = self.client.post('/auth_app/log_in/', default_data)
        self.assertEqual(test_login.status_code, 302)
        self.assertRedirects(test_login, '/polls/')

    def test_log_out(self):
        ''' Test la deconnexion
        Test the disconnection '''
        self.client.login(username="testuser2", password='testtest')
        response = self.client.get(reverse('logout'))
        self.assertIsNone(response.context)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/polls/')

    def test_signeit(self):
        ''' Test la possibilité de s'inscrire
        Test the possibility of registering '''
        default_data = {
            "username": "testuser3",
            "email": "unittest@test.com",
            "pass_first": "1234testtest",
            "pass_second": "1234testtest"}
        test_signit = self.client.post('/auth_app/signe_it/', default_data)
        self.assertEqual(test_signit.status_code, 200)
        self.assertTemplateUsed(test_signit, 'signe_it.html')

    def test_signeiterror(self):
        ''' Test si une erreur est renseigné
        Test if an error is entered '''
        default_data = {
            "username": "testuser1",
            "email": "unittest@test.com",
            "pass_first": "1234testtest",
            "pass_second": "1234testtest"}
        test_signit = self.client.post('/auth_app/signe_it/', default_data)
        self.assertEqual(test_signit.status_code, 200)
        self.assertTemplateUsed(test_signit, 'signe_it.html')


