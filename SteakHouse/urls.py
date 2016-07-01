"""SteakHouse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

'''
    Permite redireccionar todos los path que comienzan con URL:
    http://servidor/

'''

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^registro/', include('Registro.urls')),
    url(r'^perfil/',include('Perfil.urls')),
    url(r'^menu/',include('Menu.urls')),
    url(r'^billetera/',include('Billetera.urls')),
    url(r'^inventario/',include('Inventario.urls')),
    url(r'^ordenes/',include('Ordenes.urls')),
    url(r'^',include('inicio.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)