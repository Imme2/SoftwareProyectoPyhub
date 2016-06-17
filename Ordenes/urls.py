from django.conf.urls import url
from Ordenes import views


'''
    Permite redireccionar todos los path que comienzan con URL:
    http://servidor/

'''

urlpatterns = [
    url(r'^actual/$',views.verOrdenActual),
]
