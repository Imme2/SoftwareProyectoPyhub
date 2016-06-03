from django.conf.urls import url
from Menu import views

urlpatterns = [
    url(r'^editar/$',views.editarMenu),
    url(r'^editar/(?P<idMenu>[A-Za-z0-9]+)/$',views.editarMenu),
    url(r'^crear/$', views.crearMenu),
    url(r'^crearIngrediente/$', views.crearIngrediente)
]

