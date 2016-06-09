from django.shortcuts import render
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from Registro.models import perfil,proveedor,menu, ingrediente, item, posee
from django.contrib.auth.decorators import login_required
from Menu.form import formMenu, ingredienteForm, formPlato, formPosee
# Create your views here.

@login_required(login_url='/registro/login/')
def editarMenu(request, idMenu = None):
    if (not(request.user.is_staff)):
        return HttpResponseRedirect('')
    if (idMenu == None):
        listaMenus = menu.objects.all()
        return render(request,'menu/editar3.html',{'nombreMenu': "Crear un menu",
                                                 'prefijo' : 'editar',
                                                 'form': listaMenus})
    else:
        if request.method == "POST":
            formPlatos = formMenu(idMenu, data = request.POST)
            if formPlatos.is_valid():
                formPlatos.save(idMenu)
                return HttpResponseRedirect('/menu/editar/{}'.format(idMenu))
            else :
                print(formPlatos.data)
                return HttpResponseRedirect('/menu/editar/{}'.format(idMenu))                
        else:
            nombreMenu = menu.objects.get(idMenu = idMenu).nombre
            formPlatos = formMenu(idMenu)

            return render(request,'menu/editar.html', {'nombreMenu': "Editar un menu",
                                                    'form': formPlatos})

@login_required(login_url='/registro/login/')
def crearMenu(request, idMenu = None):
    if (not(request.user.is_staff)):
        return HttpResponseRedirect('/registro/logout')
    if request.method == "POST":
        formPlatos = formMenu(data = request.POST)
        if formPlatos.is_valid():
            idMenu = formPlatos.create()
            formPlatos.save(idMenu)
            return HttpResponseRedirect('/menu/editar/{}'.format(idMenu))
        else :
            print(formPlatos.data)
            return HttpResponseRedirect('/menu/crear/')                
    else:
        nombreMenu = ""
        formPlatos = formMenu()
        return render(request,'menu/editar.html', {'nombreMenu': "Crear un menu",
                                                 'form': formPlatos})

@login_required(login_url='/registro/login/')
def ingredienteView(request, idIngrediente = None):
    if (not(request.user.is_staff)):
        return HttpResponseRedirect('/registro/logout')
    if request.method == "POST":
        if idIngrediente:
            ingr = ingredienteForm(data = request.POST, instance = ingrediente.objects.get(idIngr = idIngrediente))
        else:
            ingr = ingredienteForm(data = request.POST)
        if ingr.is_valid():
            e = ingr.save()
            return HttpResponseRedirect('/menu/ingrediente/{}'.format(e.idIngr))
        else :
            return HttpResponseRedirect('/menu/ingrediente/')                
    else:
        if idIngrediente:
            form = ingredienteForm(instance = ingrediente.objects.get(idIngr = idIngrediente)) 
        else:   
            form = ingredienteForm()
        return render(request,'menu/editar.html', {'nombreMenu': "Crear ingrediente",
                                                 'form': form})


@login_required(login_url='/registro/login/')
def platoView(request, idPlato = None):
    if (not(request.user.is_staff)):
        return HttpResponseRedirect('/registro/logout')
    if request.method == "POST":
        if idPlato:
            formPlat = formPlato(data = request.POST, instance = item.objects.get(idItem = idPlato))
        else:
            formPlat = formPlato(data = request.POST)
        formPose = formPosee(data = request.POST)
        if formPlat.is_valid():
            e = formPlat.save()
            if formPose.is_valid():
                formPose.save(e)
            return HttpResponseRedirect('/menu/plato/{}'.format(e.idItem))
        else :
            return HttpResponseRedirect('/menu/plato/')                
    else:
        print("Entrando")
        if idPlato:
            platoInstance = item.objects.get(idItem = idPlato)
            formPlat = formPlato(instance = platoInstance)
            formPose = formPosee()
            form = [formPlat, formPose]
            extra = None
            extra = posee.objects.all().filter(idItem = platoInstance)
        else:   
            formPlat = formPlato()
            form = [formPlat]
            extra = None
            print("Correcto")
        return render(request,'menu/editar2.html', {'nombreMenu': "Crear plato",
                                                 'form': form,
                                                 'extra': extra})

@login_required(login_url='/registro/login/')
def platoAllView(request):
    if (not(request.user.is_staff)):
        return HttpResponseRedirect('/registro/logout')
    platos = item.objects.all()
    return render(request,'menu/editar3.html', {'nombreMenu': "Crear un menu",
                                                 'prefijo' : 'plato',
                                                 'form': platos})

@login_required(login_url='/registro/login/')
def ingredienteAllView(request):
    if (not(request.user.is_staff)):
        return HttpResponseRedirect('/registro/logout')
    ingr = ingrediente.objects.all()
    return render(request,'menu/editar3.html', {'nombreMenu': "Crear un menu",
                                                 'prefijo' : 'ingrediente',
                                                 'form': ingr})

@login_required(login_url='/registro/login/')
def quitarIngrediente(request):
    if (not(request.user.is_staff)):
        return HttpResponseRedirect('/registro/logout')
    if request.method == "GET":
        plato = request.GET.get("plato")
        ingr = request.GET.get("ingr")
        if plato and ingr:
            plato = item.objects.get(idItem = plato)
            ingr = ingrediente.objects.get(idIngr = ingr)
            posee.objects.filter(idItem = plato, idIngr = ingr).delete()
            return HttpResponseRedirect('/menu/plato/{}'.format(plato.idItem))
        else :
            return HttpResponseRedirect('/menu/plato/')                
    else:
        return HttpResponseRedirect('/menu/plato/')                
