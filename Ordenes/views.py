from django.shortcuts import render
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from Registro.views import esProveedor
from Ordenes.form import formBilleteraPagar
# Create your views here.

@login_required(login_url='/registro/login/')
def verOrdenActual(request):
    try:
        orden = request.user.ordenActual
    except:
        orden = None  
        return render(request,"ordenes/ver.html",{'monto':0})
    platos = orden.tieneRel.all()
    monto = sum(x.precio for x in platos)
    return render(request,"ordenes/ver.html",{'platos':platos,
                                                'monto':monto})


@login_required(login_url='/registro/login/')
def pagarOrdenActual(request):
    if request.user.is_staff or esProveedor(request):
        return HttpResponseRedirect('/')
    try:
        orden = request.user.ordenActual
    except:
        orden = None
        return HttpResponseRedirect('/')

    if request.method == "POST":
        formPago = formBilleteraPagar(monto = request.POST.get('monto'), data = request.POST, request = request)
        if formPago.is_valid():
            formPago.save()
            return HttpResponseRedirect('/ordenes/actual')
        return render(request,"ordenes/ver.html",{'formPago': formPago})
    else:
        platos = orden.tieneRel.all()
        monto = sum(x.precio for x in platos)
        formPago = formBilleteraPagar(monto = monto,request = request)
        return render(request,"ordenes/ver.html",{'formPago': formPago})

