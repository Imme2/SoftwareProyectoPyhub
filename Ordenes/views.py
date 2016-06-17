from django.shortcuts import render
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from Registro.models import perfil,proveedor, parametro, menu, ingrediente, item, posee
from django.contrib.auth.decorators import login_required
from Menu.form import formMenu, ingredienteForm, formPlato, formPosee
from Registro.form import parametrosForm


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
    pass
