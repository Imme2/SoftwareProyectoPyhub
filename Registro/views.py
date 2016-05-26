from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.contrib.auth import logout
from Registro.models import perfil,proveedor
from Registro.form import formRegistroProveedor, formRegistroUsuario, loginUsuario, userForm,\
    perfilForm

# Create your views here.
def registroUsuario(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/registro/login/')
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
        return HttpResponseRedirect('/registro/login/')
    if request.method == "POST":
        formUser = formRegistroUsuario(request.POST)
        formEmpr = formRegistroProveedor(request.POST)
        if formUser.is_valid() and formEmpr.is_valid():
            userEntry = formUser.save(request)
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
    if request.method == "POST":
        form = loginUsuario(request.POST)
        if form.is_valid():
            user = authenticate(username = form.cleaned_data['username'],password = form.cleaned_data['clave'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/registro/editar')
            else:
                error = ['No se pudo autenticar al usuario']
                return render(request,'registro/login.html', {'form': form,'error': error})
        else:
            return render(request,'registro/login.html', {'form': form})
    else:
        form = loginUsuario()
        return render(request,'registro/login.html', {'form': form})
    
def logOut(request):
    logout(request)
    return HttpResponseRedirect('/registro/login')






@login_required(login_url='/registro/login/')
def editarUsuario(request):
    if request.method == "POST":
        userform = userForm(instance = request.user, data = request.POST)
        profileform =  perfilForm(instance = request.user.perfil, data = request.POST)
        if userform.is_valid() and profileform.is_valid():
            userform.save(request)
            profileform.save(request)
            return HttpResponseRedirect('/registro/editar/')
        else:
            return render(request,'registro/editar.html', {'formUser': userform,
                                                          'formPerfil': profileform})
    else:
        formUser = userForm(instance = request.user)
        formPerfil = perfilForm(instance = request.user.perfil)
        return render(request,'registro/editar.html', {'formUser': formUser,
                                                      'formPerfil': formPerfil})


'''
#Para el proveedor.
@login_required(login_url='/registro/login/')
def editarUsuarioProveedor(request):
    if request.method == "POST":
        userform = userForm(instance = request.user, data = request.POST)
        profileform =  perfilForm(instance = request.user.perfil, data = request.POST)
        provedForm = 
        if userform.is_valid() and profileform.is_valid():
            userform.save(request)
            profileform.save(request)
            return HttpResponseRedirect('/registro/editar')
        else:
            return render(request,'registro/editar.html', {'formUser': userform,
                                                          'formPerfil': profileform})
    else :
        formUser = userForm(instance = request.user)
        formPerfil = perfilForm(instance = request.user.perfil)
        return render(request,'registro/editar.html', {'formUser': formUser,
'''