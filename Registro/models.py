from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class perfil(models.Model):
    Sexos = (
             ('M','Masculino'),
             ('F','Femenino'),
             )
    
    user = models.OneToOneField(User, related_name='perfil')
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
post_save.connect(create_user_profile, sender=User) #Un decorador que implica el trigger (No indentar)

class parametro(models.Model):
    idParam = models.PositiveIntegerField()
    horarioCierre = models.TimeField()
    horarioEntrada = models.TimeField()
    cantPuestos = models.PositiveIntegerField()
        
class proveedor(models.Model):
    username = models.ForeignKey(User,primary_key = True)
    nombreEmpr = models.CharField(max_length = 20)
    rif = models.CharField(max_length = 10)
    ofreceRel = models.ManyToManyField('ingrediente',through = 'ofrece')
    
class cliente(models.Model):
    username = models.ForeignKey(User,primary_key = True)
    idMenu = models.ForeignKey('menu')
    
class administrador(models.Model):
    username = models.ForeignKey(User,primary_key = True)
    idParam = models.ForeignKey('parametro')
    usernameP = models.ForeignKey('proveedor')
      
class ingrediente(models.Model):
    idIngr = models.AutoField(primary_key = True)
    cantidad = models.PositiveIntegerField()
    nombre = models.CharField(max_length = 50)

    consultaRel = models.ManyToManyField(proveedor,through = 'consulta')

class item(models.Model):
    idItem = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 50)
    tipo = models.CharField(max_length = 1)
    precio = models.PositiveIntegerField()
    foto = models.CharField(max_length = 300)
    descripcion = models.CharField(max_length = 200)

    poseeRel = models.ManyToManyField(ingrediente,through = 'posee')

    def __str__(self):
        return self.nombre

class transaccion(models.Model):
    idTrans = models.AutoField(primary_key = True)
    username = models.ForeignKey('cliente')
    monto = models.PositiveIntegerField()
    fecha = models.DateField()
    
class menu(models.Model):
    idMenu = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 50)

    contieneRel = models.ManyToManyField(item,through = 'contiene')

class orden(models.Model):
    nroOrden = models.AutoField(primary_key = True)
    fecha = models.DateField()
    
    realizaRel = models.ManyToManyField(cliente,through = 'realiza')
    tieneRel = models.ManyToManyField(item,through = 'tiene')
    
class billetera(models.Model):
    idBilletera = models.AutoField(primary_key = True)
    username = models.ForeignKey('cliente')
    nombre = models.CharField(max_length = 20)

class consulta(models.Model):
    username = models.ForeignKey('proveedor')
    idIngr = models.ForeignKey('ingrediente')
    
    class Meta:
        unique_together = ('username','idIngr')        
        
class ofrece(models.Model):
    usernameP = models.ForeignKey('proveedor')
    idIngr = models.ForeignKey('ingrediente')
    precio = models.PositiveIntegerField()
    idRest = models.PositiveIntegerField()
    
    class Meta:
        unique_together = ('usernameP','idIngr')
        
    
class pedido(models.Model):
    usernameP = models.ForeignKey('proveedor')
    usernameA = models.ForeignKey('administrador')
    idIngr = models.ForeignKey('ingrediente')
    idRest = models.PositiveIntegerField()
    
    class Meta:
        unique_together = ('usernameP','usernameA','idIngr')    

class realiza(models.Model):
    username = models.ForeignKey('cliente')
    nroOrden = models.ForeignKey('orden')
    
    class Meta:
        unique_together = ('username','nroOrden')
        
class tiene(models.Model):
    nroOrden = models.ForeignKey('orden')
    idItem = models.ForeignKey('item')
    
    class Meta:
        unique_together = ('nroOrden','idItem')
        
class contiene(models.Model):
    idMenu = models.ForeignKey('MENU')
    idItem = models.ForeignKey('item')
    
    class Meta:
        unique_together = ('idMenu','idItem')
        
class posee(models.Model):
    idItem = models.ForeignKey('item')
    idIngr = models.ForeignKey('ingrediente')

    class Meta:
        unique_together = ('idItem','idIngr')

