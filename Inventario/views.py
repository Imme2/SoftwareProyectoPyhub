from django.shortcuts import render
from Registro.views import esProveedor
from Inventario.auxfuncs import getInventarioProveedor
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect

# Create your views here.

@login_required(login_url='/registro/login/')
def mostrarInventario(request):
    if (not(esProveedor(request))):
        return HttpResponseRedirect('')

    arreglo = getInventarioProveedor(request)

    return render(request,'inventario/mostrar.html', {'ListaIngredientes':arreglo})


@login_required(login_url='/registro/login/')
def modificarInventario(request):
    if (not(esProveedor(request))):
        return HttpResponseRedirect('')
    if request.method == "POST":
        formPlatos = formMenu(idMenu, data = request.POST)
        if formPlatos.is_valid():
            formPlatos.save(idMenu)
            return HttpResponseRedirect('/menu/editar/{}'.format(idMenu))
        else:
            print(formPlatos.data)
            return HttpResponseRedirect('/menu/editar/{}'.format(idMenu))                
    else:
        nombreMenu = menu.objects.get(idMenu = idMenu).nombre
        formPlatos = formMenu(idMenu)

        return render(request,'menu/editar.html', {'nombreMenu': "Editar un menu",
                                                'form': formPlatos})
