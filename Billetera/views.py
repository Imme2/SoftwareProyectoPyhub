from django.shortcuts import render

# Create your views here.


@login_required(login_url='/registro/login/')
def crearBilletera(request):
    if request.method == "POST":
        form = billeteraAuth(request.POST)
        if form.is_valid():
            user = authenticate(username = form.cleaned_data['username'],password = form.cleaned_data['clave'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/registro/editar')
            else:
                error = ['Nombre de usuario o clave incorrectos']
                return render(request,'billetera/crear.html', {'form': form,'error': error})
        else:
            return render(request,'billetera/crear.html', {'form': form})
    else:
        form = loginUsuario()
        return render(request,'billetera/crear.html', {'form': form})