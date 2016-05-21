from django.shortcuts import render
from Registro.form import NameForm
from django.http.response import HttpResponse, HttpResponseRedirect
from Registro.models import usuario

# Create your views here.
def registro_usuario(request):
    
    if request.method == "POST":
        form = NameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            nombre = form.cleaned_data['nombre']
            apellidos = form.cleaned_data['apellidos']
            f_nac = form.cleaned_data['f_nac']
            correo = form.cleaned_data['correo']
            tlf = form.cleaned_data['tlf']
            clave = form.cleaned_data['clave']
            #sexo = forms.CharField(widget=forms.Textarea, required = False)
            ci = form.cleaned_data['ci']
            entrada = usuario(username = username, 
                              nombre = nombre, 
                              apellido = apellidos, 
                              f_nac = f_nac, 
                              correo = correo,
                              tlf = tlf,
                              clave = clave,
                              ci = ci)
            entrada.save()
            return HttpResponseRedirect('/registro')
        else:
            return render(request,'registro/usuario.html', {'form': form})
    else:
        form = NameForm()
        return render(request,'registro/usuario.html', {'form': form})