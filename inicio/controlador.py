from Registro.models import menu, item, parametro
import datetime

def getCurrentMenu():
	parametros = parametro.objects.all()
	if len(parametros) == 0:
		return None
	else:
		parametrosActuales = parametro[0]
		menuActual = parametrosActuales.menuActual
		platos = menuActual.ofreceRel.all()
		return platos
