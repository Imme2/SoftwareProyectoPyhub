from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from Billetera.form import formBilleteraCrear, formBilleteraRecargar, formTransaccion
from Registro.models import billetera

# Create your views here.


@login_required(login_url='/registro/login/')
def crearBilletera(request):
    #Check de si tiene una billetera ya.
    if billetera.objects.filter(user = request.user).exists():
        return HttpResponseRedirect('/billetera/recargar')
    if request.method == "POST":
        form = formBilleteraCrear(request.POST)
        if form.is_valid():
            form.save(request)
            return HttpResponseRedirect('/billetera/recargar')
        else:
            return render(request,'billetera/crear.html', {'form': form})
    else:
        form = formBilleteraCrear()
        return render(request,'billetera/crear.html', {'form': form})

@login_required(login_url='/registro/login/')
def recargarBilletera(request):
    return HttpResponseRedirect('/')
    if not(billetera.objects.filter(user = request.user).exists()):
        return HttpResponseRedirect('/billetera/crear')
    if request.method == "POST":
        form = formBilleteraRecargar(request.POST)
        transaccion = formTransaccion(data = request.POST)
        if transaccion.is_valid():
            monto = transaccion.save()
            if form.is_valid():
                claveDada = form.cleaned_data.get('clave')
                if (request.user.billetera.verifyPassword(claveDada)):
                    form.save()
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponseRedirect('?error=1')
        return render(request,'billetera/recargar.html', {'form': form,
                                                    'monto': transaccion,
                                                    'error': None})
    else:
        #Este error se refiere a password equivocado
        error =  request.GET.get('error',None)

        #se mandan las formas.
        form = formBilleteraRecargar()
        transaccion = formTransaccion()

        return render(request,'billetera/recargar.html', {'form': form,
                                                            'monto': transaccion,
                                                            'error':error})