from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from Registro.models import perfil,proveedor,menu
from django.contrib.auth.decorators import login_required
from Menu.form import formMenuCrear, menuSelector, formPlatoSelector
# Create your views here.


@login_required(login_url='/registro/login/')
def crearMenu(request):
    if (not(request.user.is_staff)):
        return HttpResponseRedirect('')
    if request.method == "POST":
        pass
    else:
        pass


@login_required(login_url='/registro/login/')
def editarMenu(request, idMenu = None):
    if (not(request.user.is_staff)):
        return HttpResponseRedirect('')
    if (idMenu == None):
        listaMenus = menu.objects.all()
        listaMenus = [(x.nombre,x.idMenu) for x in listaMenus]
        return render(request,'menu/escoger.html', {'listaMenu': listaMenus})
    else:
        nombreMenu = menu.objects.get(idMenu= idMenu).nombre
        formPlatos = formPlatoSelector(idMenu)
        return render(request,'menu/editar.html', {'nombreMenu': nombreMenu,
                                                    'form': formPlatos})

#def cambiarMenuEsp(request):