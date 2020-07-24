from django.urls import path
from . import views

urlpatterns = [
    path('log_in/', views.get_login, name='login'),
    path('log_out/', views.log_out, name='logout'),
    path('signe_it/', views.get_signeit, name='signeit'),
]
