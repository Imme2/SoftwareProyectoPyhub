from django.shortcuts import render
from django.http import HttpResponse
from inicio.controlador import getCurrentMenu
from inicio.form import formMostrarPlato
from django.forms import modelformset_factory
from Registro.models import parametro,item,ordenActual
from Registro.views import esProveedor

'''

Muestra el menu principal y permite hacer ordenes.

'''

def index(request):
    user = request.user
    if not(user.is_authenticated()) or user.is_staff or esProveedor(request) :
        menu = getCurrentMenu()
        return render(request,'inicio/home.html',{'menu':menu})
    if request.method == "POST":
        platos = getCurrentMenu()
        if platos is None:
            return render(request,'inicio/home.html',{'menu':None})   #Panic?
        formSetPlatos = modelformset_factory(item, form = formMostrarPlato,extra = 0)
        formSet = formSetPlatos(request.POST,request.FILES)
        if formSet.is_valid():
            for form in formSet:
                form.save(request)
            return HttpResponse('/pedidos/actual/')
        else:
            return render(request,'inicio/home.html',{'formMenu': formSet}) 
    else:
        platos = getCurrentMenu()
        if (platos is None):
            return render(request,'inicio/home.html')
        else:
            formSetPlatos = modelformset_factory(item, form = formMostrarPlato,extra = 0)
            formSet = formSetPlatos(queryset = platos)
            return render(request,'inicio/home.html',{'formMenu': formSet})