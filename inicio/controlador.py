from Registro.models import menu, item, parametro, posee
import datetime

def getCurrentMenu():
	parametros = parametro.objects.all()
	if not(parametros.exists()):
		return None
	else:
		parametrosActuales = parametros[0]
		menuActual = parametrosActuales.menuActual
		if menuActual is None:
			return None
		platos = menuActual.contieneRel.all()
		platos = list(filter(disponible, platos))
		#platos = {k:v for (k,v) in platos.items() if disponible(v.idItem)}
		return platos


def disponible(plato):
	ingredientes = posee.objects.filter(idItem = plato)
	for x in ingredientes:
		ingr = x.idIngr
		if ingr.cantidad >= x.cantidad:
			pass
		else: 
			return False
	return True
