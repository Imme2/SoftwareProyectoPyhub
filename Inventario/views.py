from django.shortcuts import render
from Registro.views import esProveedor
from Inventario.auxfuncs import getInventarioProveedor
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from Inventario.form import formOfrece, formIngredientes
# Create your views here.

@login_required(login_url='/registro/login/')
def mostrarInventario(request):
    if (not(esProveedor(request))):
        return HttpResponseRedirect('/')

    arreglo = getInventarioProveedor(request)

    return render(request,'inventario/mostrar.html', {'ListaOferta':arreglo})


@login_required(login_url='/registro/login/')
def modificarInventario(request):
    if (not(esProveedor(request))):
        return HttpResponseRedirect('/')

    if request.method == "POST":

        # Ofrece tiene unicamente el campo de precio mientras que
        # Los ingredientes se muestran como lista en la otra form
        formPrecio = formOfrece(data = request.POST)
        formIngredintes = formIngredientes(data= request.POST)
    
        if formIngredientes.is_valid():
            idIngr = formIngredientes.save()
            if formPrecio.is_valid():
                formPrecio.save(idIngr,request.user.proveedor)

        #Se crea un arreglo de todas las ofertas disponibles (Ahora con los updates)
        arregloOfertas = getInventarioProveedor(request)

        return render(request,'inventario/modificar.html', {'ListaOferta': arregloOfertas,
                                                        'formIngredientes': formIngredientes,
                                                        'formPrecio': formPrecio})
    else:
        #Se crea un arreglo de todas las ofertas disponibles
        arregloOfertas = getInventarioProveedor(request)

        # Ofrece tiene unicamente el campo de precio mientras que
        # Los ingredientes se muestran como lista en la otra form
        formPrecio = formOfrece()
        formIngredintes = formIngredientes()
        
        return render(request,'inventario/modificar.html',{'ListaOferta': arregloOfertas,
                                                            'formIngredientes': formIngredientes,
                                                            'formPrecio': formPrecio})