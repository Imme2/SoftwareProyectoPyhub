from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from Billetera.form import formBilleteraCrear, formBilleteraRecargar, formTransaccion
from Registro.models import billetera

# Create your views here.

'''
 Vista de crear billetera, se pide una clave que debe ser repetida
        para ser asociada a la billetera
'''
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

'''
 Vista de recargar billetera, actualmente no funcional, pide datos de una tarjeta
        y guarda los datos de la transaccion cuando recarga la billetera
'''
@login_required(login_url='/registro/login/')
def recargarBilletera(request):
    if not(billetera.objects.filter(user = request.user).exists()):
        return HttpResponseRedirect('/billetera/crear')
    if request.method == "POST":
        form = formBilleteraRecargar(data = request.POST,request=request)
        transaccion = formTransaccion(data = request.POST)
        if transaccion.is_valid(request) and form.is_valid():
            monto = transaccion.save()
            form.save(request,monto)
            return HttpResponseRedirect('/')
        return render(request,'billetera/recargar.html', {'form': form,
                                                    'monto': transaccion})
    else:

        #se mandan las formas.
        form = formBilleteraRecargar()
        transaccion = formTransaccion()

        return render(request,'billetera/recargar.html', {'form': form,
                                                            'monto': transaccion})