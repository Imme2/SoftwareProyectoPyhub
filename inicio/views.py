from django.shortcuts import render
from django.http import HttpResponse
from inicio.controlador import getCurrentMenu
from inicio.form import formMostrarPlato
from django.forms import modelformset_factory
from Registro.models import parametro,item



def index(request):
    parametros = parametro.objects.all()
    parametrosActuales = parametros[0]
    menuAct = parametrosActuales.menuActual
    platos = menuAct.contieneRel.all()


    formSetPlatos = modelformset_factory(item, fields= ('nombre', 'precio', 'descripcion'), form = formMostrarPlato,extra = 0)

    formSet = formSetPlatos(queryset = platos)


    return render(request,'inicio/home.html',{'menu': formSet})