from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.contrib.auth import logout
from Registro.models import perfil
from Registro.form import formRegistroUsuario, loginUsuario, userForm,\
    perfilForm

# Create your views here.
def registroUsuario(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/registro')
    if request.method == "POST":
        form = formRegistroUsuario(request.POST)
        if form.is_valid():
            
            username = form.cleaned_data['username']
            nombre = form.cleaned_data['nombre']
            apellidos = form.cleaned_data['apellidos']
            f_nac = form.cleaned_data['f_nac']
            correo = form.cleaned_data['correo']
            tlf = form.cleaned_data['tlf']
            clave = form.cleaned_data['clave']
            sexo = form.cleaned_data['sexo']
            ci = form.cleaned_data['ci']
            entry = User.objects.create_user(username= username ,email = correo, password = clave)
            entry.first_name = nombre
            entry.last_name = apellidos
            entry.save()
            p_entry = perfil.objects.get(user = entry)
            p_entry.ci = ci
            p_entry.sexo = sexo
            p_entry.fechaNac = f_nac
            p_entry.tlf = tlf
            p_entry.save()
            return HttpResponseRedirect('/registro')
        else:
            return render(request,'registro/home.html', {'form': form})
        pass
    else:
        form = formRegistroUsuario()
        return render(request,'registro/home.html', {'form': form})
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
                print("error")
                return render(request,'registro/login.html', {'form': form,'error': error})
        else:
            print("invalid form?")
            return render(request,'registro/login.html', {'form': form})
    else:
        form = loginUsuario()
        print("get")
        return render(request,'registro/login.html', {'form': form})
    
def logOut(request):
    logout(request)
    return HttpResponseRedirect('/registro/login')

@login_required(login_url='/registro/login/')
def editarUsuario(request):
    if request.method == "POST":
        userform = userForm(instance = request.user, data = request.POST)
        profileform =  perfilForm(instance = perfil.objects.get(user = request.user), data = request.POST)
        if userform.is_valid() and profileform.is_valid():
            user = userform.save(commit = False)
            user.user = request.user
            if userform.cleaned_data['password']:
                user.set_password(userform.cleaned_data['password'])
            user.save()
            profile = profileform.save(commit = False)
            profile.user = user
            profile.save()
            return HttpResponseRedirect('/registro/editar')
        else:
            return render(request,'registro/editar.html', {'formUser': userform,
                                                          'formPerfil': profileform})
    else :
        formUser = userForm(instance = request.user)
        perfils = perfil.objects.get(user = request.user)
        print(request.user.email)
        formPerfil = perfilForm(instance = perfil.objects.get(user = request.user))
        return render(request,'registro/editar.html', {'formUser': formUser,
                                                      'formPerfil': formPerfil})
