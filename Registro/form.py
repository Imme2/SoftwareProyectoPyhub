from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from Registro.models import perfil

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
    
class loginUsuario(forms.Form):
    username = forms.CharField(label='Nombre de usuario', max_length=40)
    clave = forms.CharField(widget=forms.PasswordInput())
    
# class formEditarUsuario(forms.Form):
#     phone_regex = RegexValidator(regex=r'^\+?(58)?\d{11}$', message="El numero de telefono debe tener el formato: '+5899999999999'.")
#     ci_regex = RegexValidator(regex=r'^[VP]\d{8,10}$', message="El numero de telefono debe tener el formato: '+5899999999999'.")
#      
#     username = forms.CharField(label='Nombre de usuario', max_length=40, widget=forms.TextInput(attrs={'class':'disabled', 'readonly':'readonly'}))
#     nombre = forms.CharField(label='Nombre', max_length=100)
#     apellidos = forms.CharField(label='Apellidos', max_length=100)
#     f_nac = forms.DateField(label='Fecha de nacimiento', initial=datetime.date.today)
#     correo = forms.EmailField(label = "Correo")
#     tlf = forms.CharField(validators=[phone_regex])
#     clave = forms.CharField(widget=forms.PasswordInput())
#     sexo = forms.ChoiceField(choices = perfil.Sexos, required = True)
#     ci = forms.CharField(validators=[ci_regex])
    

