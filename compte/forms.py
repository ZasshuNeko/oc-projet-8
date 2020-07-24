from django import forms
from django.core.validators import *


class SearchMenu(forms.Form):
    search = forms.CharField(
        label="", widget=forms.TextInput(
            attrs={
                'placeholder': 'Chercher'}))


class Edit(forms.Form):
    last_name = forms.CharField(
        label='Votre nom',
        required=False,
        widget=forms.TextInput,
        max_length=100,
        validators=[
            RegexValidator(
                regex="([a-zA-Z-]){4,99}",
                message="Nom invalide")])
    first_name = forms.CharField(
        label='Votre prénom',
        required=False,
        widget=forms.TextInput,
        max_length=100,
        validators=[
            RegexValidator(
                regex="([a-zA-Z-]){4,99}",
                message="Prénom invalide")])
    email = forms.EmailField(
        label='Votre courriel',
        required=False,
        max_length=200,
        validators=[
            EmailValidator()])
    pass_first = forms.CharField(
        label='Votre mot de passe',
        required=False,
        widget=forms.PasswordInput,
        max_length=100,
        validators=[
            RegexValidator(
                regex="([a-zA-Z]){4,12}([0-9]){2,12}",
                message="Mot de passe invalide")])
    pass_second = forms.CharField(
        label='Répéter votre mot de passe',
        required=False,
        widget=forms.PasswordInput,
        max_length=100,
        validators=[
            RegexValidator(
                regex="([a-zA-Z]){4,12}([0-9]){2,12}",
                message="Mot de passe invalide")])


class InfoView(forms.Form):
    last_name = forms.CharField(
        label='Votre nom',
        required=False,
        widget=forms.TextInput,
        max_length=100,
        validators=[
            RegexValidator(
                regex="([a-zA-Z-]){4,99}",
                message="Nom invalide")])
    first_name = forms.CharField(
        label='Votre prénom',
        required=False,
        widget=forms.TextInput,
        max_length=100,
        validators=[
            RegexValidator(
                regex="([a-zA-Z-]){4,99}",
                message="Prénom invalide")])
    email = forms.EmailField(
        label='Votre courriel',
        required=False,
        max_length=200,
        validators=[
            EmailValidator()])
