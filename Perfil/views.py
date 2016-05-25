from django.shortcuts import render
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from Registro.models import perfil,proveedor

# Create your views here.


@login_required(login_url='/registro/login/')
def mostrarPerfil(request):
    if (request.user.has_perm('proveedor')):
        return HttpResponseRedirect('/perfil/proveedor')
    else:
        return HttpResponseRedirect('/perfil/usuario')

@login_required(login_url='/registro/login/')
def mostrarPerfilUsuario(request):
    if (request.user.has_perm('proveedor')):
        return HttpResponseRedirect('/perfil/proveedor')

    user = request.user
    perfil = perfil.objects.get(username = user.username)

    return render(request,'/perfil/mostrar.html',{'Username': user.username,
                                                    'Email': user.email,
                                                    'Nombre': user.first_name,
                                                    'Apellido': user.last_name,
                                                    'CI': perfil.ci,
                                                    'Sexo': perfil.sexo,
                                                    'Fecha de Nacimiento': perfil.f_nac
                                                    'Telefono': perfil.tlf})



@login_required(login_url='/registro/login/')
def mostrarPerfilproveedor(request):
    if (!request.user.has_perm('proveedor')):
        return HttpResponseRedirect('/perfil/usuario')

    user = request.user
    perfil = perfil.objects.get(username = user.username)
    

    return render(request,'/perfil/mostrar.html',{'Username': user.username,
                                                    'Email': user.email,
                                                    'Nombre': user.first_name,
                                                    'Apellido': user.last_name,
                                                    'CI': perfil.ci,
                                                    'Sexo': perfil.sexo,
                                                    'Fecha de Nacimiento': perfil.f_nac
                                                    'Telefono': perfil.tlf})

