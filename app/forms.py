from django import forms
from django.core.validators import *


class Search(forms.Form):
    search = forms.CharField(
        label="", widget=forms.TextInput(
            attrs={
                'placeholder': 'Chercher'}))


class SearchMenu(forms.Form):
    search = forms.CharField(
        label="", widget=forms.TextInput(
            attrs={
                'placeholder': 'Chercher'}))


class MultiSelect(forms.Form):
    select_produit = forms.ChoiceField(widget=forms.Select(), choices=(
        ['liste produit supplémentaire']), initial='0', required=True,)
