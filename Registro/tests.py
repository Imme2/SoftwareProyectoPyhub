from django.test import TestCase
from django.contrib.auth.models import User
from Registro.models import *
from django.test import Client
from decimal import Decimal
from datetime import date

class perfilTestCase(TestCase):
	
	def setUp(self):
		usr = User.objects.create_user(
			username="guillermo_bet",
			email="11-10103@usb.ve",
			password="passwd",
			first_name="Guillermo",
			last_name="Betancourt"
		)
		usr.perfil.ci="24492586"
		usr.perfil.sexo="M"
		usr.perfil.tlf="04141234567"
		usr.perfil.save()
		self.c = Client()

	def tearDown(self):
		usr = perfil.objects.get(ci="24492586")
		usr.delete()
		self.c = None

	def testNombrePerfil(self):
		u = perfil.objects.get(ci="24492586")
		self.assertEqual(u.user.first_name, "Guillermo")

	def testApellidoPerfil(self):
		u = perfil.objects.get(ci="24492586")
		self.assertEqual(u.user.last_name, "Betancourt")

	def testCorreoPerfil(self):
		u = perfil.objects.get(ci="24492586")
		self.assertEqual(u.user.email, "11-10103@usb.ve")

	def testClavePerfil(self):
		u = perfil.objects.get(ci="24492586")
		self.assertEqual(u.user.check_password("passwd"),True)

	def testUsuarioPerfil(self):
		u = perfil.objects.get(ci="24492586")
		self.assertEqual(u.user.username, "guillermo_bet")

	def testSexoPerfil(self):
		u = perfil.objects.get(ci="24492586")
		self.assertEqual(u.sexo, "M")

	def testTelefonoPerfil(self):
		u = perfil.objects.get(ci="24492586")
		self.assertEqual(u.tlf, "04141234567")

	def testLoginDatabase(self):
		login=self.c.login(username="guillermo_bet", password="passwd")
		self.assertEqual(login, True)

# ----------------------------------------------------

class ingredienteTestCase(TestCase):

	def setUp(self):
		i = ingrediente.objects.create(
			cantidad=5,
			nombre="Tomate"
		)
		i.save()

	def tearDown(self):
		i = ingrediente.objects.get(idIngr=1)
		i.delete()

	def testCantidadIngrediente(self):
		i = ingrediente.objects.get(idIngr=1)
		self.assertEqual(i.cantidad, 5)

	def textNombreIngrediente(self):
		i = ingrediente.objects.get(idIngr=1)
		self.assertEqual(i.nombre, "Tomate")

# ----------------------------------------------------

class itemTestCase(TestCase):

	def setUp(self):
		i = item.objects.create(
				nombre="Panquecas",
				tipo="p",
				precio="1200.5",
				foto="/home/usr/images/photo.jpg",
				descripcion="Panquecas de vainilla con miel"
			)
		"""
		m = menu.objects.create(
				nombre='Menu ejecutivo'

			)
		
		c = User.objects.create_user(
				username="guillermo_bet",
				email="11-10103@usb.ve",
				password="passwd",
				first_name="Guillermo",
				last_name="Betancourt"
			)
		
		c.cliente.idMenu = 
		"""		
		i.save()

	def tearDown(self):
		i = item.objects.get(idItem=1)
		i.delete()

	def testNombreItem(self):
		i = item.objects.get(idItem=1)
		self.assertEqual(i.nombre, "Panquecas")

	def testTipoItem(self):
		i = item.objects.get(idItem=1)
		self.assertEqual(i.tipo, "p")

	def testPrecioItem(self):
		i = item.objects.get(idItem=1)
		self.assertEqual(i.precio, Decimal("1200.500"))

	def testPathFotoItem(self):
		i = item.objects.get(idItem=1)
		self.assertEqual(i.foto, "/home/usr/images/photo.jpg")

	def testDescripcionItem(self):
		i = item.objects.get(idItem=1)
		self.assertEqual(i.descripcion, "Panquecas de vainilla con miel")

# ----------------------------------------------------

"""
class transaccionTestCase(TestCase):
	def setUp(self):
		t = transaccion.objects.create(	
				monto="1000.30",
				fecha=date(2016, 1, 1)
			)
		t.save()

	def tearDown(self):
		t = transaccion.objects.get(idTrans=1)
		t.delete()

	def testMontoTransaccion(self):
		t = transaccion.objects.get(idTrans=1)
		self.assertEqual(t.monto, Decimal("1000.300"))

	def testFechaTransaccion(self):
		t.transaccion.objects.get(idTrans=1)
		self.assertEqual(t.fecha, date(2016, 1, 1))

class proveedorTestCase(TestCase):

	def setUp(self):
		self.i = ingrediente.objects.create(
			cantidad=5,
			nombre="Tomate"
		)
		self.i.save()

		self.p = proveedor(
			username=User.objects.create_user(
			username="guillermo_bet",
			email="11-10103@usb.ve",
			password="passwd",
			first_name="Guillermo",
			last_name="Betancourt"
			)
		)
		self.p.nombreEmpr="PyHop"
		self.p.rif="J294660487"
		#p.ofreceRel = ofrece(
			#usernameP=proveedor.objects.get(rif="J294660487"),
			#idIngr=ingrediente.objects.get(idIngr="1"),
			#precio=100#,
			#idRest=1
		#)
		self.p.save()

	def tearDown(self):
		self.p.delete()
		self.i.delete()

	def testNombreProveedor(self):
		p = proveedor.objects.get(rif="J294660487")
		self.assertEqual(self.p.first_name, "Guillermo")
"""
# ----------------------------------------------------

class responseTestCase(TestCase):

	def setUp(self):
		self.c = Client()

	def tearDown(self):
		self.c = None

	def testResponseServidor(self):
		response=self.c.post("/")
		self.assertEqual(response.status_code, 200)
