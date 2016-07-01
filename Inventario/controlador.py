from Registro.models import billetera, proveedor, ingrediente, ofrece, tiene, item
from django.contrib.auth.models import User, Permission

#Pre: El usuario en request es un proveedor
#Post: Retorna None si esta vacio, sino una lista de los nombres y los precios de los ingredientes
def getInventarioProveedor(request):
	if (ofrece.objects.filter(usernameP = request.user.proveedor).exists()):
		ofertas = ofrece.objects.filter(usernameP = request.user.proveedor)
		arregloOfertas = [[x.idIngr.nombre,x.precio] for x in ofertas]
		return arregloOfertas
	else:
		return None


def calcularIngredientesMasPedidos():

	ingredientesPedidos = tiene.objects.all()

	auxMapa = {}

	for x in ingredientesPedidos:
		if x.item.idItem in auxMapa:
			auxMapa[x.item.idItem] += x.cantidad
		else:
			auxMapa[x.item.idItem] = x.cantidad


	# Se buscan todos los items para ahorrarnos repetidos accesos a la base de datos
	todosLosItems = item.objects.all()

	mapaIngredientes = {}
	mapaNombres = {}

	for x in auxMapa:
		aux = todosLosItems.get(idItem = x)
		for relacion in aux.poseeRel.all():
			idIngr = relacion.idIngr
			if idIngr in mapaIngredientes:
				mapaIngredientes[idIngr] += relacion.cantidad*auxMapa[x]
			else:
				mapaIngredientes[idIngr] = relacion.cantidad*auxMapa[x]
				mapaNombres[idIngr] = relacion.nombre


	ListaIngredientes = []

	for x in mapaIngredientes:
		ListaIngredientes += [{'nombre': mapaNombres[x], 'cantidad': mapaIngredientes[x]}]

	sorted(ListaIngredientes, key = lambda c: c['cantidad'])


	return ListaIngredientes