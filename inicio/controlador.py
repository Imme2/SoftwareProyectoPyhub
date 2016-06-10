from Registro.models import menu, item, parametro
import datetime

def getCurrentMenu(request):
	try:
		parametros = parametro.objects.all()
		parametrosActuales = parametro[0]
		menuActual = parametrosActuales.menuActual
		platos = menuActual.ofreceRel.all()
		return [[x.nombre,x.precio,x.descripcion] for x in platos]
	except:
		return None