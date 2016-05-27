from django.shortcuts import render
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from Registro.models import perfil,proveedor
from django.contrib.auth.decorators import login_required
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
                                                    'Fecha de Nacimiento': perfil.f_nac,
                                                    'Telefono': perfil.tlf})



@login_required(login_url='/registro/login/')
def mostrarPerfilProveedor(request):
    if (not(request.user.has_perm('proveedor'))):
        return HttpResponseRedirect('/perfil/usuario')

    user = request.user
    perfil = perfil.objects.get(username = user.username)
    prov = proveedor.objects.get(username = user.username)

    return render(request,'/perfil/mostrar.html',{'Username': user.username,
                                                    'Email': user.email,
                                                    'Nombre': user.first_name,
                                                    'Apellido': user.last_name,
                                                    'CI': perfil.ci,
                                                    'Sexo': perfil.sexo,
                                                    'Fecha de Nacimiento': perfil.f_nac,
                                                    'Telefono': perfil.tlf,
                                                    'RIF': prov.rif,
                                                    'Nombre de Empresa': prov.nombreEmpr})




#INCOMPLETA NO USAR TODAIVA.
@login_required(login_url='/registro/login/')
def mostarUsuarios(request):
    if (not(request.user.is_staff)):
        return HttpResponseRedirect('')

    listaUsuarios = User.objects.all()
    listaPerfil = perfil.objects.all()

    return render(request,'/perfil/mostrarUsuarios.html',{'ListaUsuarios': listaUsuarios})