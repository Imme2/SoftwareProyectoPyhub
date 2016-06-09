from django.conf.urls import url
from Menu import views
'''
	Permite redireccionar todos los path que comienzan con URL:
	http://servidor/menu/

'''
urlpatterns = [
    url(r'^editar/$',views.editarMenu),
    url(r'^editar/(?P<idMenu>[A-Za-z0-9]+)/$',views.editarMenu),
    url(r'^crear/$', views.crearMenu),
    url(r'^ingrediente/(?P<idIngrediente>[0-9]+)?$', views.ingredienteView),
    url(r'^ingredientes/$', views.ingredienteAllView),
    url(r'^plato/(?P<idPlato>[0-9]+)?$', views.platoView),
    url(r'^platos/$', views.platoAllView),
    url(r'^plato/eliminarIngr.*', views.quitarIngrediente),
    url(r'^parametros/$', views.parametrosView)
]

