from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from Registro.models import perfil,proveedor,menu
from django.contrib.auth.decorators import login_required
from Menu.form import menuCrear, menuSelector, platoSelector
# Create your views here.

'''
@login_required(login_url='/registro/login/')
def crearMenu(request):
    if (not(request.user.is_admin())):
#       return HttpResponseRedirect(request,'/'):
    if request.method == "POST":
        pass
    else:
        pass
'''

@login_required(login_url='/registro/login/')
def editarMenu(request, idMenu = None):
    if (not(request.user.is_staff)):
        return HttpResponseRedirect('')
    if (idMenu == None):
        listaMenus = menu.objects.all()
        listaMenus = [x.nombre for x in listaMenus]
        return render(request,'menu/escoger.html', {'listaMenu': formMenus})
    else:
        nombreMenu = menu.objects.get(idMenu= idMenu).nombre
        formPlatos = platoSelector(idMenu)

        return render(request,'menu/editar.html', {'nombreMenu': nombreMenu,
                                                    'form': formPlatos})

#def cambiarMenuEsp(request):