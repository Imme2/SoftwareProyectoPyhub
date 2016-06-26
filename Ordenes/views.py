from django.shortcuts import render
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from Registro.views import esProveedor
from Ordenes.form import formBilleteraPagar, ingredientesPedido, formResena
from Registro.models import tieneActual,resena

@login_required(login_url='/registro/login/')
def verOrdenActual(request, errores = None):
    try:
        orden = request.user.ordenActual
    except:
        orden = None  
        return render(request,"ordenes/ordenar.html",{'monto':0})

    errores = ingredientesPedido(request.user)
    platos = tieneActual.objects.filter(orden = orden)
    monto = sum(x.item.precio * x.cantidad for x in platos)

    platos = [{'precio':x.item.precio,
                'nombre':x.item.nombre,
                'descripcion':x.item.descripcion,
                'cantidad':x.cantidad} for x in platos]
    return render(request,"ordenes/ordenar.html",{'platos':platos,
                                                'monto':monto,
                                                'error': errores})


'''

Funcion para pagar la orden actual, verifica que tengas una orden y una billetera
   y te da la opcion de cancelar tu orden actual (pagar el balance).

'''
@login_required(login_url='/registro/login/')
def pagarOrdenActual(request):
    if request.user.is_staff or esProveedor(request):
        return HttpResponseRedirect('/')
    try:
        orden = request.user.ordenActual       # Se chequea que tenga una orden abierta.
        request.user.billetera                 # Se chequea que se tenga una billetera.
    except:
        orden = None
        return HttpResponseRedirect('/')

    if request.method == "POST":
        formPago = formBilleteraPagar(monto = request.POST.get('monto'), request = request)
        formReview = formResena(data = request.POST)
        if request.META.get('HTTP_REFERER').split("/")[-2] != "actual":
            formPago = formBilleteraPagar(monto = request.POST.get('monto'), data = request.POST, request = request)
            if formPago.is_valid():
                valor = formPago.save()
                if valor[0] == 'error': 
                    return verOrdenActual(request, errores = valor[1])
                elif valor[0] == 'valid':
                    if formReview.is_valid():
                        formReview.save(orden = valor[1])
                    return HttpResponseRedirect('/ordenes/actual')
        return render(request,"ordenes/pagar.html",{'formPago': formPago,
                                                    'formResena': formReview})
    else:
        platos = tieneActual.objects.filter(orden = orden)
        monto = sum(x.item.precio*x.cantidad for x in platos)
        formPago = formBilleteraPagar(monto = monto,request = request)
        formReview = formResena()
        return render(request,"ordenes/pagar.html",{'formPago': formPago,
                                                    'formResena': formReview})

@login_required(login_url='/registro/login/')
def verReviews(request):
    if not(request.user.is_staff):
        return HttpResponseRedirect('/')
    

    todasResenas = resena.objects.all()

    listaResenas = [{"resena":x.contenido,
                        "nombre":x.orden.user.username,
                        "orden":x.orden.tieneRel.all(),
                        "fecha":x.orden.fecha}
                                        for x in todasResenas]

    print(listaResenas)

    return render(request,"ordenes/verReviews.html",{'listaResenas': listaResenas})
