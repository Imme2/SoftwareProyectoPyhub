from Registro.models import menu, item, parametro
import datetime

def getCurrentMenu():
	try:
		parametros = parametro.objects.all()
		parametrosActuales = parametro[0]
		menuActual = parametrosActuales.menuActual
		platos = menuActual.ofreceRel.all()
		return platos
	except:
		return None