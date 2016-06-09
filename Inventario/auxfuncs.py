from Registro.models import billetera, proveedor, ingrediente, ofrece
from django.contrib.auth.models import User, Permission


#Pre: El usuario en request es un proveedor
def getInventarioProveedor(request):
	if (ofrece.objects.filter(usernameP = request.user.proveedor).exists()):
		ofertas = ofrece.objects.filter(usernameP = request.user.proveedor)
		arregloOfertas = [[x.idIngr.nombre,x.precio] for x in ofertas]
		return arregloOfertas
	else:
		return None
