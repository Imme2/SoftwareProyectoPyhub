'''
Created on May 21, 2016

@author: David Hernandez
'''
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
