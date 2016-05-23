from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class perfil(models.Model):
    Sexos = (
             ('M','Masculino'),
             ('F','Femenino'),
             )
    
    user = models.ForeignKey(User, unique=True)
    ci = models.CharField(max_length = 10, blank=True, null=True)
    sexo = models.CharField(max_length = 1, choices = Sexos, blank=True, null=True)
    fechaNac = models.DateField(blank=True, null=True)
    foto = models.CharField(max_length = 300,blank=True, null=True)
    tlf = models.CharField(max_length = 11,blank=True, null=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
    
    def __unicode__(self):
        return self.user
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        perfil.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)

class parametro(models.Model):
    idParam = models.PositiveIntegerField()
    horarioCierre = models.TimeField()
    horarioEntrada = models.TimeField()
    cantPuestos = models.PositiveIntegerField()
        
class proveedor(models.Model):
    username = models.ForeignKey(User,primary_key = True)
    nombreEmpr = models.CharField(max_length = 20)
    rif = models.CharField(max_length = 10)
    ofreceRel = models.ManyToManyField('INGREDIENTE',through = 'OFRECE')
    
class cliente(models.Model):
    username = models.ForeignKey(User,primary_key = True)
    idMenu = models.ForeignKey('MENU')
    
class administrador(models.Model):
    username = models.ForeignKey(User,primary_key = True)
    idParam = models.ForeignKey('PARAMETRO')
    usernameP = models.ForeignKey('PROVEEDOR')
      
class ingrediente(models.Model):
    idIngr = models.PositiveIntegerField(primary_key = True)
    cantidad = models.PositiveIntegerField()
    nombre = models.CharField(max_length = 50)

    consultaRel = models.ManyToManyField(proveedor,through = 'CONSULTA')

class item(models.Model):
    idItem = models.PositiveIntegerField(primary_key = True)
    nombre = models.CharField(max_length = 50)
    tipo = models.CharField(max_length = 1)
    precio = models.PositiveIntegerField()
    foto = models.CharField(max_length = 300)
    descripcion = models.CharField(max_length = 200)

    poseeRel = models.ManyToManyField(ingrediente,through = 'POSEE')

class transaccion(models.Model):
    idTrans = models.PositiveIntegerField(primary_key = True)
    username = models.ForeignKey('CLIENTE')
    monto = models.PositiveIntegerField()
    fecha = models.DateField()
    
class menu(models.Model):
    idMenu = models.PositiveIntegerField(primary_key = True)
    nombre = models.CharField(max_length = 50)

    contieneRel = models.ManyToManyField(item,through = 'CONTIENE')

class orden(models.Model):
    nroOrden = models.PositiveIntegerField(primary_key = True)
    fecha = models.DateField()
    
    realizaRel = models.ManyToManyField(cliente,through = 'REALIZA')
    tieneRel = models.ManyToManyField(item,through = 'TIENE')
    
class billetera(models.Model):
    idBilletera = models.PositiveIntegerField(primary_key = True)
    username = models.ForeignKey('CLIENTE')
    nombre = models.CharField(max_length = 20)

class consulta(models.Model):
    username = models.ForeignKey('PROVEEDOR')
    idIngr = models.ForeignKey('INGREDIENTE')
    
    class Meta:
        unique_together = ('username','idIngr')        
        
class ofrece(models.Model):
    usernameP = models.ForeignKey('PROVEEDOR')
    idIngr = models.ForeignKey('INGREDIENTE')
    precio = models.PositiveIntegerField()
    idRest = models.PositiveIntegerField()
    
    class Meta:
        unique_together = ('usernameP','idIngr')
        
    
class pedido(models.Model):
    usernameP = models.ForeignKey('PROVEEDOR')
    usernameA = models.ForeignKey('ADMINISTRADOR')
    idIngr = models.ForeignKey('INGREDIENTE')
    idRest = models.PositiveIntegerField()
    
    class Meta:
        unique_together = ('usernameP','usernameA','idIngr')    

class realiza(models.Model):
    username = models.ForeignKey('CLIENTE')
    nroOrden = models.ForeignKey('ORDEN')
    
    class Meta:
        unique_together = ('username','nroOrden')
        
class tiene(models.Model):
    nroOrden = models.ForeignKey('ORDEN')
    idItem = models.ForeignKey('ITEM')
    
    class Meta:
        unique_together = ('nroOrden','idItem')
        
class contiene(models.Model):
    idMenu = models.ForeignKey('MENU')
    idItem = models.ForeignKey('ITEM')
    
    class Meta:
        unique_together = ('idMenu','idItem')
        
class posee(models.Model):
    idItem = models.ForeignKey('ITEM')
    idIngr = models.ForeignKey('INGREDIENTE')

    class Meta:
        unique_together = ('idItem','idIngr')

