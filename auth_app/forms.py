from django import forms
from django.core.validators import *


class SearchMenu(forms.Form):
    search = forms.CharField(
        label="", widget=forms.TextInput(
            attrs={
                'placeholder': 'Chercher'}))


class LogIn(forms.Form):
    log_id = forms.CharField(label='Identifiant', max_length=100)
    pwd = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(),
        max_length=100)


class SignIt(forms.Form):
    password = False
    username = forms.CharField(label='Nom du compte', max_length=30)
    pass_first = forms.CharField(
        label='Votre mot de passe',
        widget=forms.PasswordInput,
        max_length=100,
        validators=[
            RegexValidator(
                regex="([a-zA-Z]){4,12}([0-9]){2,12}",
                message="Mot de passe invalide")])
    pass_second = forms.CharField(
        label='Répéter votre mot de passe',
        widget=forms.PasswordInput,
        max_length=100,
        validators=[
            RegexValidator(
                regex="([a-zA-Z]){4,12}([0-9]){2,12}",
                message="Mot de passe invalide")])
    email = forms.EmailField(
        label='Votre courriel',
        max_length=200,
        validators=[
            EmailValidator()])
