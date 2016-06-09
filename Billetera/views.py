from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from Billetera.form import formBilleteraCrear
from Registro.models import billetera

# Create your views here.


@login_required(login_url='/registro/login/')
def crearBilletera(request):
    #Check de si tiene una billetera ya.
    if billetera.objects.filter(user = request.user).exists():
        return HttpResponseRedirect('Billetera/recargar')
    if request.method == "POST":
        form = formBilleteraCrear(request.POST)
        if form.is_valid():
            form.save(request)
            return HttpResponseRedirect('Billetera/recargar')
        else:

            return render(request,'billetera/crear.html', {'form': form})
    else:
        form = formBilleteraCrear()
        return render(request,'billetera/crear.html', {'form': form})

@login_required(login_url='/registro/login/')
def recargarBilletera(request):
    pass