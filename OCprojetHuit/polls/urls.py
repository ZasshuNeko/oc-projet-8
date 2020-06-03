from django.urls import path, re_path

from . import views

urlpatterns = [
	path('',views.index, name='index'),
	path('log_in/', views.get_login, name='login'),
	path('log_out/', views.log_out, name='logout'),
	path('signe_it/', views.get_signeit, name='signeit'),
	path('get_compte/', views.get_compte, name='compte'),
	path('get_aliments/',views.get_aliments, name='aliments')
	path('resultat/',views.get_resultat, name='resultat')

]

#Faire un r_path pour déterminer si c'est un utilisateur demander une auth puis sur /polls/UTIL donner accès au compte
# sur polls/util/edit donner accès au formulaire d'édition du compte