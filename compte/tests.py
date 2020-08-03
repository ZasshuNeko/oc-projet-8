from django.test import TestCase
from django.urls import reverse
from polls.models import Produits, Favoris
from django.contrib.auth.models import User

from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Create your tests here.


class TestApp(TestCase):
    """ Mise en place des tests """

    def setUp(self):
        """ Mise en place des bases de données """
        test_user1 = User.objects.create_user(
            username="testuser1",
            password='testtest',
            email="test@test.com")
        test_user2 = User.objects.create_user(
            username="testuser2", password='testtest')

        test_user1.save()
        test_user2.save()

        id_produit1 = Produits.objects.get(pk=1)
        id_produit2 = Produits.objects.get(pk=2)

        test_favoris = Favoris.objects.create(
            user=test_user1,
            produits=id_produit1,
            date_ajout="08/06/2020",
            aff_index=False)
        test_favoris.save()
        test_favoris = Favoris.objects.create(
            user=test_user2,
            produits=id_produit1,
            date_ajout="08/06/2020",
            aff_index=False)
        test_favoris.save()
        test_favoris = Favoris.objects.create(
            user=test_user2,
            produits=id_produit2,
            date_ajout="08/06/2020",
            aff_index=False)
        test_favoris.save()
        test_favoris = Favoris.objects.create(
            user=test_user1,
            produits=id_produit1,
            date_ajout="08/06/2020",
            aff_index=False)
        test_favoris.save()

    def test_not_log(self):
        response = self.client.get('/compte/get_compte/testuser2/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '/auth_app/log_in/?next=/compte/get_compte/testuser2/')

    def test_compte(self):
        self.client.login(username="testuser1", password='testtest')
        response = self.client.get(reverse('login'))

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')

        test_edit = self.client.get(
            '/compte/get_compte/' + str(response.context['user']) + '/')
        self.assertEqual(test_edit.status_code, 200)
        self.assertTemplateUsed(test_edit, 'compte.html')
        self.assertEqual(str(test_edit.context['data']['name']), str(
            response.context['user']))

    def test_compteedit(self):
        self.client.login(username="testuser1", password='testtest')
        response = self.client.get(reverse('login'))

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')

        test_edit = self.client.get(
            '/compte/get_compte/' + str(response.context['user']) + '/edit/')
        self.assertEqual(test_edit.status_code, 200)
        self.assertTemplateUsed(test_edit, 'compte_edit.html')

    def test_change_info(self):
        self.client.login(username="testuser1", password='testtest')
        response = self.client.get(reverse('login'))

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')

        default_data = {
            "last_name": "TestDjango",
            "first_name": "TestDjangoFirst",
            "email": "Test@test.test"}

        test_edit = self.client.post(
            '/compte/get_compte/' + str(response.context['user']) + '/valide/', default_data)
        self.assertEqual(test_edit.status_code, 302)

        test_edit = self.client.get(
            '/compte/get_compte/' + str(response.context['user']) + '/')
        self.assertEqual(test_edit.status_code, 200)
        self.assertEqual(
            str(test_edit.context['data']['name']), "TestDjangoFirst TestDjango")
        
