from django.conf.urls import url
from . import views

'''
	Permite redireccionar todos los path que comienzan con URL:
	http://servidor/

'''

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
