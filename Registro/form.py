from django import forms
from django.core.validators import RegexValidator
from Registro.models import usuario
import datetime

class formRegistroUsuario(forms.Form):
    phone_regex = RegexValidator(regex=r'^\+?(58)?\d{11}$', message="El numero de telefono debe tener el formato: '+5899999999999'.")
    ci_regex = RegexValidator(regex=r'^[VP]\d{8,10}$', message="El numero de telefono debe tener el formato: '+5899999999999'.")
    
    username = forms.CharField(label='Nombre de usuario', max_length=40)
    nombre = forms.CharField(label='Nombre', max_length=100)
    apellidos = forms.CharField(label='Apellidos', max_length=100)
    f_nac = forms.DateField(label='Fecha de nacimiento', initial=datetime.date.today)
    correo = forms.EmailField(label = "Correo")
    tlf = forms.CharField(validators=[phone_regex])
    clave = forms.CharField(widget=forms.PasswordInput())
    sexo = forms.ChoiceField(choices = usuario.Sexos, required = True)
    ci = forms.CharField(validators=[ci_regex])
    
class formEditarUsuario(forms.Form):
    phone_regex = RegexValidator(regex=r'^\+?(58)?\d{11}$', message="El numero de telefono debe tener el formato: '+5899999999999'.")
    ci_regex = RegexValidator(regex=r'^[VP]\d{8,10}$', message="El numero de telefono debe tener el formato: '+5899999999999'.")
    
    username = forms.CharField(label='Nombre de usuario', max_length=40, widget=forms.TextInput(attrs={'class':'disabled', 'readonly':'readonly'}))
    nombre = forms.CharField(label='Nombre', max_length=100)
    apellidos = forms.CharField(label='Apellidos', max_length=100)
    f_nac = forms.DateField(label='Fecha de nacimiento', initial=datetime.date.today)
    correo = forms.EmailField(label = "Correo")
    tlf = forms.CharField(validators=[phone_regex])
    clave = forms.CharField(widget=forms.PasswordInput())
    sexo = forms.ChoiceField(choices = usuario.Sexos, required = True)
    ci = forms.CharField(validators=[ci_regex])
    
class loginUsuario(forms.Form):
    username = forms.CharField(label='Nombre de usuario', max_length=40)
    clave = forms.CharField(widget=forms.PasswordInput())