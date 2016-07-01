from django.shortcuts import render
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from Registro.models import perfil,proveedor, orden
from django.contrib.auth.decorators import login_required
from Registro.views import esProveedor

'''
    Controlador para redireccionar la vista de perfil
'''

@login_required(login_url='/registro/login/')
def mostrarPerfil(request):
    if (esProveedor(request) and not(request.user.is_staff)):
        return HttpResponseRedirect('/perfil/proveedor')
    else:
        return HttpResponseRedirect('/perfil/usuario')

'''
   Controlador que muestra perfil a usuarios
'''

@login_required(login_url='/registro/login/')
def mostrarPerfilUsuario(request):
    if (esProveedor(request) and not(request.user.is_staff) ):
        return HttpResponseRedirect('/perfil/proveedor')

    user = request.user
    perfill = user.perfil

    print(perfill.foto)

    return render(request,'Perfil/mostrar.html',{'Username': user.username,
                                                    'Email': user.email,
                                                    'Nombre': user.first_name,
                                                    'Apellido': user.last_name,
                                                    'CI': perfill.ci,
                                                    'Sexo': perfill.sexo,
                                                    'FechaDeNacimiento': perfill.fechaNac,
                                                    'Telefono': perfill.tlf,
                                                    'Foto':perfill.foto})

'''
      Controlador que muestra perfil a proveedores
'''

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



'''
      Controlador para mostrar todos los usuarios registrados
'''
# Para mostrar todos los usuarios a un admin
@login_required(login_url='/registro/login/')
def mostrarUsuarios(request):
    if (not(request.user.is_staff)):
        return HttpResponseRedirect('/')

    listaUsuarios = User.objects.all()
    listaUsuarios = [[x.username, x.first_name, x.last_name, x.perfil, x.has_perm('auth.proveedor')]\
                     for x in listaUsuarios]
    print(listaUsuarios)
    return render(request,'Perfil/mostrarUsuarios.html',{'ListaUsuarios': listaUsuarios})

# Para mostrar todas las transacciones a un admin
@login_required(login_url='/registro/login/')
def mostrarTransacciones(request):
    if (not(request.user.is_staff)):
        return HttpResponseRedirect('/')
    ordenes = orden.objects.all()
    return render(request,'Perfil/mostrarTransacciones.html',{'ordenes': ordenes})
    