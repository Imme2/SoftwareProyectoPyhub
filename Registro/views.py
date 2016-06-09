from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.contrib.auth.models import User, Permission
from django.contrib.auth import logout
from Registro.models import perfil,proveedor
from Registro.form import formRegistroProveedor, formRegistroUsuario, loginUsuario, userForm,\
    perfilForm, proveedorForm


#A ser movido proximamente
def esProveedor(request):
    if request.user.has_perm('auth.proveedor'):
        return True
    else:
        return False

# Vista de registro de usuario, verifica que el usuario no este autenticado primero.
def registroUsuario(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/perfil/')
    if request.method == "POST":
        form = formRegistroUsuario(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/registro/login/')
        else:
            return render(request,'registro/cliente.html', {'form': form})
    else:
        form = formRegistroUsuario()
        return render(request,'registro/cliente.html', {'form': form})



def registroProveedor(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/perfil/')
    if request.method == "POST":
        formUser = formRegistroUsuario(request.POST)
        formEmpr = formRegistroProveedor(request.POST)
        if formUser.is_valid() and formEmpr.is_valid():
            userEntry = formUser.save()
            formEmpr.save(request,userEntry)
            return HttpResponseRedirect('/registro/login/')
        else:
            return render(request,'registro/proveedor.html', {'formUser': formUser,
                                                                'formEmpr': formEmpr})
        pass
    else:
        formUser = formRegistroUsuario()
        formEmpr = formRegistroProveedor()
        return render(request,'registro/proveedor.html', {'formUser': formUser,
                                                                'formEmpr': formEmpr})

# 
# 
# Formulario de logeo para usuarios
def logearUsuario(request):
    #Se captura el argumento en caso de haber uno (en caso de no haberlo se coloca el string vacio)
    next = request.GET.get('next','')
    if request.method == "POST":
        form = loginUsuario(request.POST)
        if form.is_valid():
            user = authenticate(username = form.cleaned_data['username'],password = form.cleaned_data['clave'])
            if user is not None:
                login(request, user)
                if (next == ''):
                    return HttpResponseRedirect('/perfil/')
                else:
                    return HttpResponseRedirect(next)
            else:
                error = ['Nombre de usuario o clave incorrectos']
                return render(request,'registro/login.html', {'form': form,'error': error})
        else:
            return render(request,'registro/login.html', {'form': form})
    else:
        if not request.user.is_authenticated():
            form = loginUsuario()
            return render(request,'registro/login.html', {'form': form})
        if (next == ''):
            return HttpResponseRedirect('/perfil/')
        else:
            return HttpResponseRedirect(next)  

  
def logOut(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='/registro/login/')
def editarDatos(request):
    if (esProveedor(request)):
        return HttpResponseRedirect('/registro/editar/proveedor')
    else:
        return HttpResponseRedirect('/registro/editar/usuario')


@login_required(login_url='/registro/login/')
def editarUsuario(request):
    if (esProveedor(request)):
        return HttpResponseRedirect('/registro/editar/proveedor')
    if request.method == "POST":
        userform = userForm(instance = request.user, data = request.POST)
        profileform =  perfilForm(instance = request.user.perfil, data = request.POST)
        if userform.is_valid() and profileform.is_valid():
            userform.save(request)
            profileform.save(request)
            return HttpResponseRedirect('/perfil/usuario')
        else:
            return render(request,'registro/editarUsuario.html', {'formUser': userform,
                                                          'formPerfil': profileform})
    else:
        formUser = userForm(instance = request.user)
        formPerfil = perfilForm(instance = request.user.perfil)
        return render(request,'registro/editarUsuario.html', {'formUser': formUser,
                                                      'formPerfil': formPerfil})



#Para el proveedor.
@login_required(login_url='/registro/login/')
def editarProveedor(request):
    if (not(esProveedor(request))):
        return HttpResponseRedirect('/registro/editar/Usuario')
    if request.method == "POST":
        userform = userForm(instance = request.user, data = request.POST)
        profileform = perfilForm(instance = request.user.perfil, data = request.POST)
        try:
            provedForm = proveedorForm(instance = request.user.proveedor, data=request.POST)
        except:
            provedForm = proveedorForm()

        if userform.is_valid() and profileform.is_valid() and provedForm.is_valid():
            userform.save(request)
            profileform.save(request)
            return HttpResponseRedirect('/perfil/')
        else:
            return render(request,'registro/editarProveedor.html', {'formUser': userform,
                                                          'formPerfil': profileform,
                                                          'formProveedor': provedForm})
    else:
        formUser = userForm(instance = request.user)
        formPerfil = perfilForm(instance = request.user.perfil)
        try:
            formProveedor = proveedorForm(instance = proveedor.objects.get(username = request.user))
        except:
            formProveedor = proveedorForm()

        return render(request,'registro/editarProveedor.html', {'formUser': formUser,
                                                                'formPerfil':formPerfil,
                                                                'formProveedor':formProveedor})
