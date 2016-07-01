from django.shortcuts import render
from django.http import HttpResponseRedirect
from inicio.controlador import getCurrentMenu
from inicio.form import formMostrarPlato
from django.forms import modelformset_factory
from Registro.models import parametro,item,ordenActual, orden, resena
from Registro.views import esProveedor

def expandir(item):
    item.resena = [x.contenido for x in resena.objects.all() if item in x.orden.tieneRel.all()]
    item.resena = item.resena[-3:]
    return item

'''

Muestra el menu principal y permite hacer ordenes.

'''

def index(request):
    user = request.user
    if not(user.is_authenticated()) or user.is_staff or esProveedor(request) :
        menu = getCurrentMenu()
        menu = list(map(expandir,menu))
        return render(request,'inicio/home.html',{'menu':menu})
    if request.method == "POST":
        platos = getCurrentMenu()
        if platos is None:
            return render(request,'inicio/home.html',{'menu':None})   #Panic?
        platosResena = list(map(expandir,platos))
        formSetPlatos = modelformset_factory(item, form = formMostrarPlato,extra = 0)
        formSet = formSetPlatos(request.POST,request.FILES)
        if formSet.is_valid():
            for form in formSet:
                form.save(request)
            return HttpResponseRedirect('/ordenes/actual/')
        else:
            return render(request,'inicio/home.html',{'formMenu': formSet, 'platos': platosResena}) 
    else:
        platos = getCurrentMenu()
        if (platos is None):
            return render(request,'inicio/home.html')
        else:
            platosResena = list(map(expandir,platos))
            formSetPlatos = modelformset_factory(item, form = formMostrarPlato,extra = 0)
            formSet = formSetPlatos(queryset = platos)
            return render(request,'inicio/home.html',{'formMenu': formSet, 'platos': platosResena})