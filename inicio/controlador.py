from Registro.models import menu, item, parametro
import datetime

def getCurrentMenu():
	parametros = parametro.objects.all()
	if not(parametros.exists()):
		return None
	else:
		parametrosActuales = parametros[0]
		menuActual = parametrosActuales.menuActual
		platos = menuActual.contieneRel.all()
		return platos
