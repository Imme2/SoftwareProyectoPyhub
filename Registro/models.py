from django.db import models
import datetime

# Create your models here.
class usuario(models.Model):
    username = models.CharField(max_length = 40)
    nombre = models.CharField(max_length = 40, blank=True)
    apellido = models.CharField(max_length = 40, blank=True)
    f_nac = models.DateField(blank=True, default = datetime.date.today)
    correo = models.EmailField(blank=True)
    tlf = models.CharField(max_length = 20, blank=True)
    clave = models.CharField(max_length = 20, blank=True)
   # sexo = forms.CharField(widget=forms.Textarea, required = False)
    sexo = models.CharField(max_length = 20, blank=True)
    ci = models.CharField(max_length = 20, blank=True)
    
    def __str__(self):
        return self.nombre + " " + self.apellido
    