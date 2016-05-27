from django.conf.urls import url
from Perfil import views

urlpatterns = [
     url(r'^$', views.mostrarPerfil),
     url(r'^proveedor/', views.mostrarPerfilProveedor),
     url(r'^usuario/', views.mostrarPerfilUsuario)
]
