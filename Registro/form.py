from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from Registro.models import perfil, proveedor
import datetime
 

def dateValidator(value):
    if value >= datetime.date.today():
        raise ValidationError(
            _('¡La fecha de Nacimiento no puede ser en el futuro!'),
            params={'value': value},
        )


class formRegistroUsuario(forms.Form):
    phone_regex = RegexValidator(regex=r'^\+?(58)?\d{11,14}$', message="El numero de telefono debe tener el formato: '+5899999999999'.")
    ci_regex = RegexValidator(regex=r'^[VP]\d{8,10}$', message="El numero de telefono debe tener el formato: '+5899999999999'.")
    username_regex = RegexValidator(regex = r'^([A-Za-z]|\d|\.|\_)*$',message = "Tu Username solo puede contener caracteres alphanumericos, puntos (.) o pisos (_). No se aceptan espacios.")
    nombres_regex = RegexValidator(regex = r'^[A-Za-z]{4,41}$', message = "Un Nombre o Apellido solo puede contener letras del alfabeto")

    username = forms.CharField(validators = [username_regex], label='Nombre de usuario', max_length=40)
    nombre = forms.CharField(validators = [nombres_regex], label='Nombre', max_length=100)
    apellidos = forms.CharField(validators = [nombres_regex],label='Apellidos', max_length=100)
    f_nac = forms.DateField(validators = [dateValidator],label='Fecha de nacimiento', initial=datetime.date.today)
    correo = forms.EmailField(label = "Correo")
    tlf = forms.CharField(validators=[phone_regex])
    clave = forms.CharField(widget=forms.PasswordInput())
    sexo = forms.ChoiceField(choices = perfil.Sexos, required = True)
    ci = forms.CharField(validators=[ci_regex])
    
    def clean(self):
        cleaned_data = super(formRegistroUsuario, self).clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        ci = cleaned_data.get('ci')

        if User.objects.filter(username=username).exists():
            msg = "El nombre de usuario ya esta utilizado"
            self.add_error('username', msg)
            
        if User.objects.filter(email=email).exists():
            msg = "El correo ya esta utilizado"
            self.add_error('correo', msg)
    
        if perfil.objects.filter(ci=ci).exists():
            msg = "Esta CI ya esta registrada"
            self.add_error('correo', msg)
            
        return cleaned_data

class formRegistroProveedor(forms.Form):
    nombreEmpresa_regex = RegexValidator(regex = r'^[A-Za-z]{4,41}$', message = "El Nombre de la empresa solo puede contener letras del alfabeto")

    rif = forms.CharField(validators = [], label ='RIF', max_length = 20)
    nombreEmpresa = forms.CharField(validators = [],label = 'Nombre de la Empresa', max_length = 40)

    def clean(self):
        cleaned_data = super(formRegistroProveedor, self).clean()
        rif = cleaned_data.get('rif')
        nombreEmpresa = cleaned_data.get('nombreEmpresa')

        if proveedor.objects.filter(rif=rif).exists():
            msg = "Este rif ya esta registrado."
            self.add_error('rif', msg)
            
        if proveedor.objects.filter(nombreEmpr=nombreEmpresa).exists():
            msg = "Este nombre de empresa ya esta registrado."
            self.add_error('nombreEmpresa', msg)
    
        return cleaned_data

    
class loginUsuario(forms.Form):
    username = forms.CharField(label='Nombre de usuario', max_length=40)
    clave = forms.CharField(widget=forms.PasswordInput())
    
    
class userForm(forms.ModelForm):
    username = forms.CharField(disabled = True, label = 'Nombre de usuario')
    first_name = forms.CharField(disabled = True, label = 'Nombre')
    last_name = forms.CharField(disabled = True, label = 'Apellido')
    email = forms.EmailField(disabled = True, label = 'Correo')
    password = forms.CharField(widget=forms.PasswordInput(), label = 'Contrasena', required = False)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']
        
class perfilForm(forms.ModelForm):
    fechaNac = forms.DateField(disabled = True, label = 'Fecha de nacimiento')
    tlf = forms.CharField(label = 'Numero de telefono')
    ci = forms.CharField(disabled = True, label = 'CI')
    class Meta:
        model = perfil
        exclude = ('user',) 


