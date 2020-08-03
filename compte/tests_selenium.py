from django.test import TestCase
from django.urls import reverse
from polls.models import Produits, Favoris
from django.contrib.auth.models import User

from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class AccountTestCase(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox(
            executable_path='webdriver\\geckodriver.exe')
        super(AccountTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(AccountTestCase, self).tearDown()

    def test_editcompte(self):
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get('http://127.0.0.1:8000/auth_app/log_in/')
        # find the form element
        username = selenium.find_element_by_id('id_log_id')
        password = selenium.find_element_by_id('id_pwd')

        submit = selenium.find_element_by_name('login')

        # Fill the form with data
        username.send_keys('TestSelenium')
        password.send_keys('test123456')

        # submitting the form
        submit.send_keys(Keys.RETURN)
        selenium.implicitly_wait(10)
        name_index = "Bonjour TestSelenium"
        # check the returned result
        self.assertEqual(selenium.find_element_by_css_selector(
            "h1#info_login").get_attribute("innerHTML").splitlines()[0], name_index)

        selenium.get(
            'http://127.0.0.1:8000/compte/get_compte/TestSelenium/edit/')

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

        self.assertEqual(selenium.find_element_by_id(
            "first").get_attribute("value"), "TestSelenium")
        self.assertEqual(selenium.find_element_by_id(
            "last").get_attribute("value"), "Django_test")