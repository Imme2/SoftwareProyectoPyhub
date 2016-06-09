from django.conf.urls import url
from Inventario import views

urlpatterns = [
     url(r'^mostrar/$', views.mostrarInventario),
]