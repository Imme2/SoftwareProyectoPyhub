from django.shortcuts import render
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from Registro.models import perfil,proveedor
from django.contrib.auth.decorators import login_required
from Registro.views import esProveedor
# Create your views here.




@login_required(login_url='/registro/login/')
def mostrarPerfil(request):
    if (esProveedor(request)):
        return HttpResponseRedirect('/perfil/proveedor')
    else:
        return HttpResponseRedirect('/perfil/usuario')

@login_required(login_url='/registro/login/')
def mostrarPerfilUsuario(request):
    if (esProveedor(request)):
        return HttpResponseRedirect('/perfil/proveedor')

    user = request.user
    perfill = perfil.objects.get(user = user.username)

    return render(request,'/perfil/mostrar.html',{'Username': user.username,
                                                    'Email': user.email,
                                                    'Nombre': user.first_name,
                                                    'Apellido': user.last_name,
                                                    'CI': perfill.ci,
                                                    'Sexo': perfill.sexo,
                                                    'Fecha de Nacimiento': perfill.f_nac,
                                                    'Telefono': perfill.tlf})



@login_required(login_url='/registro/login/')
def mostrarPerfilProveedor(request):
    if (not(esProveedor(request))):
        return HttpResponseRedirect('/perfil/usuario')

    user = request.user
    perfil = perfil.objects.get(user = user.username)
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




# Para mostrar todos los usuarios a un admin
@login_required(login_url='/registro/login/')
def mostrarUsuarios(request):
    if (not(request.user.is_staff)):
        return HttpResponseRedirect('')

    listaPerfil = perfil.objects.all()
    listaPerfil = [[x.user.username, x.user.first_name, x.user.last_name, x.ci] for x in listaPerfil]

    return render(request,'/perfil/mostrarUsuarios.html',{'ListaUsuarios': listaPerfil})