from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from Registro.models import perfil
from Registro.form import formRegistroUsuario, loginUsuario

# Create your views here.
def registroUsuario(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/registro')
    if request.method == "POST":
        form = formRegistroUsuario(request.POST)
        if form.is_valid():
            ### Verficacion de repetidos
            error = []
            user_c = User.objects.filter(username = form.cleaned_data['username']).count()
            correo_c = User.objects.filter(email = form.cleaned_data['correo']).count()
            ci_c = perfil.objects.filter(ci = form.cleaned_data['ci']).count()
            if user_c > 0:
                error.append("El nombre de usuario ya esta utilizado")
            if correo_c > 0:
                error.append("El correo ya esta utilizado")
            if ci_c > 0:
                error.append("Esta CI ya esta registrada")
            if len(error) > 0:    
                return render(request,'registro/home.html', {'form': form, 'error' : error})
            ### Validacion finalizada
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
                return HttpResponseRedirect('registro/editar')
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
