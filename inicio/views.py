from django.shortcuts import render
from django.http import HttpResponse
from inicio.controlador import getCurrentMenu
from inicio.form import formMostrarPlato
from django.forms import modelformset_factory
from Registro.models import parametro,item



def index(request):
    if request.method == "POST":
        platos = getCurrentMenu()
        formSetPlatos = modelformset_factory(item, form = formMostrarPlato,extra = 0)
        formSet = formSetPlatos(queryset = platos, data = request.POST)
        return render(request,'inicio/home.html',{'menu': formSet})
    else:
        platos = getCurrentMenu()
        if (platos is None):
            return render(request,'inicio/home.html')
        else:
            formSetPlatos = modelformset_factory(item, form = formMostrarPlato,extra = 0)
            formSet = formSetPlatos(queryset = platos)
            return render(request,'inicio/home.html',{'menu': formSet})