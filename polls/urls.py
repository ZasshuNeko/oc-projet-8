from django.urls import path, re_path

from . import views

urlpatterns = [
	path('',views.index, name='index'),
	path('log_in/', views.get_login, name='login'),
	path('log_out/', views.log_out, name='logout'),
	path('signe_it/', views.get_signeit, name='signeit'),
]