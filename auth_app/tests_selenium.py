from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class AccountTestCase(LiveServerTestCase):
    ''' Test Selenium '''

    def setUp(self):
        ''' Mise en place des paramètres
        Setting parameters '''
        self.selenium = webdriver.Firefox(
            executable_path='webdriver\\geckodriver.exe')
        super(AccountTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(AccountTestCase, self).tearDown()

    def test_register(self):
        ''' Appel la page d'enregistrement
        Call up the registration page '''
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get('http://127.0.0.1:8000/auth_app/signe_it/')
        # find the form element
        username = selenium.find_element_by_id('id_username')
        email = selenium.find_element_by_id('id_email')
        password1 = selenium.find_element_by_id('id_pass_first')
        password2 = selenium.find_element_by_id('id_pass_second')

        submit = selenium.find_element_by_name('register')

        # Fill the form with data
        username.send_keys('TestSelenium')
        email.send_keys('yusuf@qawba.com')
        password1.send_keys('test123456')
        password2.send_keys('test123456')

        # submitting the form
        submit.send_keys(Keys.RETURN)
        selenium.implicitly_wait(10)

        # check the returned result
        self.assertEqual(selenium.find_element_by_css_selector("p#information").get_attribute(
            "innerHTML").splitlines()[0], "Vous avez maintenant un compte sur notre site")

    def test_signeUp(self):
        ''' Test de connexion
        Connection test '''
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