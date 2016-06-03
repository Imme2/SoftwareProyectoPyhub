from django.conf.urls import url
from Billetera import views

urlpatterns = [
     url(r'^crear/$', views.crearBilletera),
]