from django.urls import path, re_path
from django.conf.urls import handler404

from . import views

urlpatterns = [
    path(
        '',
        views.index,
        name='index'),
    re_path(
        r'^resultat/([0-9a-zA-Z\s\w]+)/$',
        views.get_resultat,
        name='resultat'),
    re_path(
        r'^id/resultat/$',
        views.get_resultat_id,
        name='resultat_id'),
    path(
        'r/resultat/',
        views.redirect_resultat,
        name='redirect_resultat'),
    path(
        'favoris/',
        views.save_favoris,
        name='favoris'),
    re_path(
        r'^maj/index/([0-9]+)/',
        views.mise_index,
        name="maj_index"),
    re_path(
        r'^aliments/([0-9]+)/',
        views.get_aliment,
        name='get_aliment'),
    re_path(
        r'^save/([0-9]+)/',
        views.save,
        name='save'),
    path(
        'mlegale/',
        views.mlegale,
        name="mention"),
]

handler404 = views.redirect_404



