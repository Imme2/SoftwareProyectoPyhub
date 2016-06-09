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
    perfill = user.perfil

    return render(request,'Perfil/mostrar.html',{'Username': user.username,
                                                    'Email': user.email,
                                                    'Nombre': user.first_name,
                                                    'Apellido': user.last_name,
                                                    'CI': perfill.ci,
                                                    'Sexo': perfill.sexo,
                                                    'FechaDeNacimiento': perfill.fechaNac,
                                                    'Telefono': perfill.tlf})



@login_required(login_url='/registro/login/')
def mostrarPerfilProveedor(request):
    if (not(esProveedor(request))):
        return HttpResponseRedirect('/perfil/usuario')


    user = request.user
    perfil = user.perfil
    prov = user.proveedor
    return render(request,'Perfil/mostrarProveedor.html',{'Username': user.username,
                                                    'Email': user.email,
                                                    'Nombre': user.first_name,
                                                    'Apellido': user.last_name,
                                                    'CI': perfil.ci,
                                                    'Sexo': perfil.sexo,
                                                    'FechaDeNacimiento': perfil.fechaNac,
                                                    'Telefono': perfil.tlf,
                                                    'RIF': prov.rif,
                                                    'NombreDeEmpresa': prov.nombreEmpr})




# Para mostrar todos los usuarios a un admin
@login_required(login_url='/registro/login/')
def mostrarUsuarios(request):
    if (not(request.user.is_staff)):
        return HttpResponseRedirect('')

    listaPerfil = perfil.objects.all()
    listaPerfil = [[x.user.username, x.user.first_name, x.user.last_name, x.ci] for x in listaPerfil]

    return render(request,'Perfil/mostrarUsuarios.html',{'ListaUsuarios': listaPerfil})