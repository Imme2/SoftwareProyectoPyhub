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
        orden = request.user.OrdenActual
    except:
        orden = None
        return render()



@login_required(login_url='/registro/login/')
def pagarOrdenActual(request):
    pass