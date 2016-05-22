from django.shortcuts import render
from Registro.form import NameForm
from django.http.response import HttpResponseRedirect
from Registro.models import usuario

# Create your views here.
def registroUsuario(request):
    if request.method == "POST":
        form = NameForm(request.POST)
        if form.is_valid():
            ### Verficacion de repetidos
            error = []
            user_c = usuario.objects.filter(username = form.cleaned_data['username']).count()
            correo_c = usuario.objects.filter(correo = form.cleaned_data['correo']).count()
            ci_c = usuario.objects.filter(ci = form.cleaned_data['ci']).count()
            if user_c > 0:
                error.append("El nombre de usuario ya esta utilizado")
            if correo_c > 0:
                error.append("El correo ya esta utilizado")
            if ci_c > 0:
                error.append("Esta CI ya esta registrada")
            if len(error) > 0:    
                return render(request,'registro/usuario.html', {'form': form, 'error' : error})
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
            entrada = usuario(username = username, 
                              nombre = nombre, 
                              apellido = apellidos, 
                              fechaNac = f_nac, 
                              correo = correo,
                              tlf = tlf,
                              clave = clave,
                              sexo = sexo,
                              ci = ci)
            entrada.save()
            return HttpResponseRedirect('/registro')
        else:
            return render(request,'registro/usuario.html', {'form': form})
    else:
        form = NameForm()
        return render(request,'registro/usuario.html', {'form': form})
