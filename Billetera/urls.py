from django.conf.urls import url
from Billetera import views


'''
	Permite redireccionar todos los path que comienzan con URL:
	http://servidor/billetera/

'''

urlpatterns = [
     url(r'^crear/$', views.crearBilletera),
]