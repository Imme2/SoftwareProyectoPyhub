from django.conf.urls import url
from Menu import views

urlpatterns = [
    url(r'^editar/$',views.editarMenu),
    url(r'^editar/(?P<idMenu>[A-Za-z0-9]+)/$',views.editarMenu),
    url(r'^crear/$', views.crearMenu),
    url(r'^ingrediente/(?P<idIngrediente>[0-9]+)?$', views.ingredienteView),
    url(r'^plato/(?P<idPlato>[0-9]+)?$', views.platoView),
    url(r'^plato/eliminarIngr.*', views.quitarIngrediente)
]

