from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from Registro.models import perfil,proveedor,menu
from django.contrib.auth.decorators import login_required
from Menu.form import formMenuCrear, menuSelector, formPlatoSelector
# Create your views here.

@login_required(login_url='/registro/login/')
def editarMenu(request, idMenu = None):
    if (not(request.user.is_staff)):
        return HttpResponseRedirect('')
    if (idMenu == None):
        listaMenus = menu.objects.all()
        return render(request,'menu/escoger.html', {'listaMenu': listaMenus})
    else:
        if request.method == "POST":
            formPlatos = formPlatoSelector(idMenu, data = request.POST)
            if formPlatos.is_valid():
                formPlatos.save(idMenu)
                return HttpResponseRedirect('/menu/editar/{}'.format(idMenu))
            else :
                print(formPlatos.data)
                return HttpResponseRedirect('/menu/editar/{}'.format(idMenu))                
        else:
            nombreMenu = menu.objects.get(idMenu = idMenu).nombre
            formPlatos = formPlatoSelector(idMenu)

            return render(request,'menu/editar.html', {'nombreMenu': "Editar un menu",
                                                    'form': formPlatos})

@login_required(login_url='/registro/login/')
def crearMenu(request, idMenu = None):
    if (not(request.user.is_staff)):
        return HttpResponseRedirect('/registro/logout')
    if request.method == "POST":
        formPlatos = formPlatoSelector(data = request.POST)
        if formPlatos.is_valid():
            idMenu = formPlatos.create()
            formPlatos.save(idMenu)
            return HttpResponseRedirect('/menu/editar/{}'.format(idMenu))
        else :
            print(formPlatos.data)
            return HttpResponseRedirect('/menu/crear/')                
    else:
        nombreMenu = ""
        formPlatos = formPlatoSelector()
        return render(request,'menu/editar.html', {'nombreMenu': "Crear un menu",
                                                 'form': formPlatos})
