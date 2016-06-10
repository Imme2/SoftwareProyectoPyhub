from django.shortcuts import render
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from Registro.models import perfil,proveedor, parametro, menu, ingrediente, item, posee
from django.contrib.auth.decorators import login_required
from Menu.form import formMenu, ingredienteForm, formPlato, formPosee
from Registro.form import parametrosForm
import datetime


@login_required(login_url='/registro/login/')
def editarMenu(request, idMenu = None):
    if (not(request.user.is_staff)):
        return HttpResponseRedirect('/registro/logout')
    if (idMenu == None):
        listaMenus = menu.objects.all()
        return render(request,'menu/editar3.html',{'Titulo': "Menúes",
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

            return render(request,'menu/editar.html', {'Titulo': "Editar un menu",
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
        return render(request,'menu/editar.html', { 'Titulo':"Crear Menu",
                                                    'form': formPlatos})

@login_required(login_url='/registro/login/')
def parametrosView(request):
    if (not(request.user.is_staff)):
        return HttpResponseRedirect('/registro/logout')
    if request.method == "POST":
        print(parametro.objects.get(idParam = 1))
        formPara = parametrosForm(instance = parametro.objects.get(idParam = 1), data = request.POST)
        if formPara.is_valid():
            formPara.save()
            return HttpResponseRedirect('/menu/parametros/')  
        else:
            print(formPara.errors)
            return render(request, 'menu/editar.html', {'Titulo': "Configurar Parametros",
                                                    'form' : formPara})
    else:
        query = parametro.objects.filter(idParam = 1)
        if not query.exists():
            g = parametro.objects.create(idParam = 1, 
                                        horarioCierre = datetime.datetime.now().time(), 
                                        horarioEntrada = datetime.datetime.now().time(),
                                        cantPuestos = 0)
        else:
            g = query[0]
        formPara = parametrosForm(instance = g)
        return render(request, 'menu/editar.html', {'Titulo': "Configurar Parametros",
                                                    'form' : formPara})


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
        return render(request,'menu/editar.html', {'Titulo': "Ingrediente",
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
            if not formPlat.is_valid():
                formPlat = formPlato(data = request.POST)
                form = [formPlat]
                extra = None
                return render(request,'menu/editar2.html', {'Titulo': "Crear Plato",
                                                     'form': form,
                                                     'extra': extra})
    else:
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
        return render(request,'menu/editar2.html', {'Titulo': "Crear plato",
                                                 'form': form,
                                                 'extra': extra})

@login_required(login_url='/registro/login/')
def platoAllView(request):
    if (not(request.user.is_staff)):
        return HttpResponseRedirect('/registro/logout')
    platos = item.objects.all()
    return render(request,'menu/editar3.html', {'Titulo': "Platos",
                                                 'prefijo' : 'plato',
                                                 'eliminar' : 'eliminarPlato',
                                                 'form': platos})

@login_required(login_url='/registro/login/')
def ingredienteAllView(request):
    if (not(request.user.is_staff)):
        return HttpResponseRedirect('/registro/logout')
    ingr = ingrediente.objects.all()
    return render(request,'menu/editar3.html', {'Titulo': "Ingredientes",
                                                 'prefijo' : 'ingrediente',
                                                 'form': ingr})

@login_required(login_url='/registro/login/')
def eliminar(request):
    redireccion = '/menu/platos/'
    if (not(request.user.is_staff)):
        return HttpResponseRedirect('/registro/logout')
    if request.method == "GET":
        plato = request.GET.get("plato")
        ingr = request.GET.get("ingrediente")
        men = request.GET.get("editar")
        if plato:
            item.objects.filter(idItem = plato).delete()
        if ingr:
            ingrediente.objects.filter(idIngr = ingr).delete()
        if men:
            menu.objects.filter(idMenu = men).delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))        
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

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
