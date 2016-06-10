from django.conf.urls import url
from Perfil import views


'''
	Permite redireccionar todos los path que comienzan con URL:
	http://servidor/perfil/

'''

urlpatterns = [
     url(r'^$', views.mostrarPerfil),
     url(r'^proveedor/', views.mostrarPerfilProveedor),
     url(r'^usuario/', views.mostrarPerfilUsuario),
     url(r'^usuarios/', views.mostrarUsuarios)
]
