from django.urls import path, re_path
from django.conf.urls import handler404

from . import views

urlpatterns = [
	path('',views.index, name='index'),
	path('log_in/', views.get_login, name='login'),
	path('log_out/', views.log_out, name='logout'),
	path('signe_it/', views.get_signeit, name='signeit'),
	path('get_compte/', views.get_compte, name='compte'),
	re_path(r'^resultat/([0-9a-zA-Z]+)/',views.get_resultat, name='resultat'),
	path('r/resultat/',views.redirect_resultat, name='redirect_resultat'),
	re_path(r'^aliments/([0-9]+)/',views.get_aliment, name='get_aliment'),
	re_path(r'^save/([0-9]+)/',views.save, name='save'),

]

handler404 = views.redirect_404

#Faire un r_path pour déterminer si c'est un utilisateur demander une auth puis sur /polls/UTIL donner accès au compte
# sur polls/util/edit donner accès au formulaire d'édition du compte