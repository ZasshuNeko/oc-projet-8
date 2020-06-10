from django.urls import path, re_path
from django.conf.urls import handler404

from . import views

urlpatterns = [
	re_path(r'^get_compte/([0-9a-zA-Z]+/$)', views.get_compte, name='compte'),
	re_path(r'^get_compte/([0-9a-zA-Z]+)/edit/', views.edit_compte, name='edit_compte'),
	re_path(r'^get_compte/([0-9a-zA-Z]+)/valide/', views.edit_valide, name='edit_valide'),
]
