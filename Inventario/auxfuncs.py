from Registro.models import billetera, proveedor, ingrediente, ofrece
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
