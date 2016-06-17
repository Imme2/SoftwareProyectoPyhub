from django.shortcuts import render
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from Registro.views import esProveedor
from Ordenes.form import formBilleteraPagar
from Registro.models import tieneActual
# Create your views here.

@login_required(login_url='/registro/login/')
def verOrdenActual(request):
    try:
        orden = request.user.ordenActual
    except:
        orden = None  
        return render(request,"ordenes/ordenar.html",{'monto':0})
    platos = tieneActual.objects.filter(orden = orden)
    monto = sum(x.item.precio*x.cantidad for x in platos)

    platos = [{'precio':x.item.precio,
                'nombre':x.item.nombre,
                'descripcion':x.item.descripcion,
                'cantidad':x.cantidad} for x in platos if x.cantidad > 0]
    return render(request,"ordenes/ordenar.html",{'platos':platos,
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
        formPago = formBilleteraPagar(monto = request.POST.get('monto'), request = request)
        if request.META.get('HTTP_REFERER').split("/")[-2] != "actual":
            formPago = formBilleteraPagar(monto = request.POST.get('monto'), data = request.POST, request = request)
            if formPago.is_valid():
                formPago.save()
                return HttpResponseRedirect('/ordenes/actual')
        print("Clave")
        return render(request,"ordenes/pagar.html",{'formPago': formPago})
    else:
        platos = tieneActual.objects.filter(orden = orden)
        monto = sum(x.item.precio*x.cantidad for x in platos)
        formPago = formBilleteraPagar(monto = monto,request = request)
        return render(request,"ordenes/pagar.html",{'formPago': formPago})

