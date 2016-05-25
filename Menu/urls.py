from django.conf.urls import url
from Menu import views

urlpatterns = [
    url(r'^editar$', views.editarMenu),
]
