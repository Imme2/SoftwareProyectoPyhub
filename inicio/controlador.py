from Registro.models import menu, item, parametro
import datetime

def getCurrentMenu():
	parametros = parametro.objects.all()
	if len(parametros) == 0:
		return None
	else:
		parametrosActuales = parametros[0]
		menuActual = parametrosActuales.menuActual
		platos = menuActual.contieneRel.all()
		return platos
