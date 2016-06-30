from django.shortcuts import render
from Registro.views import esProveedor
from Registro.models import tiene
from Inventario.controlador import getInventarioProveedor, calcularIngredientesMasPedidos
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from Inventario.form import formOfrece, formIngredientes
# Create your views here.


'''
 Vista simple de mostrar el Inventario. Muestra todas las ofertas que tiene
    el proveedor actual
'''
@login_required(login_url='/registro/login/')
def mostrarInventario(request):
    if (not(esProveedor(request))):
        return HttpResponseRedirect('/')

    arreglo = getInventarioProveedor(request)

    return render(request,'inventario/mostrar.html', {'ListaOferta':arreglo})


'''
 Vista de modificar Inventario. usa fomularios con una lista de ingredientes y un precio.
    Intentar agregar un elemento con precio 0 solo elimina uno de existirlo.
'''
@login_required(login_url='/registro/login/')
def modificarInventario(request):
    if (not(esProveedor(request))):
        return HttpResponseRedirect('/')

    if request.method == "POST":

        # Ofrece tiene unicamente el campo de precio mientras que
        # Los ingredientes se muestran como lista en la otra form
        formPrecio = formOfrece(data = request.POST)
        listaIngredientes = formIngredientes(data= request.POST)
    
        if listaIngredientes.is_valid():
            idIngr = listaIngredientes.save()
            if formPrecio.is_valid():
                formPrecio.save(idIngr,request.user.proveedor)

        #Se crea un arreglo de todas las ofertas disponibles (Ahora con los updates)
        arregloOfertas = getInventarioProveedor(request)

        return HttpResponseRedirect('/inventario/modificar/')
    else:
        #Se crea un arreglo de todas las ofertas disponibles
        arregloOfertas = getInventarioProveedor(request)

        # Ofrece tiene unicamente el campo de precio mientras que
        # Los ingredientes se muestran como lista en la otra form
        formPrecio = formOfrece()
        listaIngredientes = formIngredientes()
        
        return render(request,'inventario/modificar.html',{'ListaOferta': arregloOfertas,
                                                            'formIngredientes': listaIngredientes,
                                                            'formPrecio': formPrecio})

@login_required(login_url='/registro/login/')
def verIngredientesMasPedidos(request):
    if (not(esProveedor(request))):
        return HttpResponseRedirect('/')

    # Se obtienen todos los objetos que estan en ordenes
    IngrMasPedidos = calcularIngredientesMasPedidos()

    # Se obtienen los 5 mas pedidos
    IngrMasPedidos[:5]

    #Y se retornan a la vista
    return render(request, 'inventario/maspedidos.html',{'ListaMasPedidos':IngrMasPedidos})