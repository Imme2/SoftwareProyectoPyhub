# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from Registro.models import usuario
import datetime

# Validators (Escritos por mi)

def dateValidator(value):
    if value >= datetime.date.today():
        raise ValidationError(
            _('¡La fecha de Nacimiento no puede ser en el futuro!'),
            params={'value': value},
        )




class formRegistroUsuario(forms.Form):
    phone_regex = RegexValidator(regex=r'^\+?(58)?\d{11}$', message="El número de teléfono debe tener el formato: '+5899999999999'.")
    ci_regex = RegexValidator(regex=r'^[VE]\d{8,10}$', message="La Cédula de detidad debe tener el formato: V123456789.")
    username_regex = RegexValidator(regex = r'^([A-Za-z]|\d|\.|\_|\-)*$',message = "Tu Username solo puede contener caracteres alphanumericos, puntos (.) o pisos (_). No se aceptan espacios.")
    nombres_regex = RegexValidator(regex = '^[A-Za-z]*$', message = "Un Nombre o Apellido solo puede contener letras del alfabeto")


    nombre = forms.CharField(widget=forms.TextInput(attrs={'type':'text' ,'class':'form-control' ,'id':'inputName', 'placeholder':'Fulano',}),validators = [nombres_regex], max_length=100)
    apellidos = forms.CharField(widget=forms.TextInput(attrs={'type':'text' ,'class':'form-control' ,'id':'inputApellido', 'placeholder':'Detal',}),validators = [nombres_regex], max_length=100)
    ci = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control", 'id':"inputCedula", 'placeholder':"V123456789",}),validators=[ci_regex], label='Cédula')
    f_nac = forms.DateField(widget=forms.DateInput(attrs={'type':"date", 'class':"form-control", 'id':"inputF_Nac",}),label='Fecha de Nacimiento',validators= [dateValidator] ,initial=datetime.date.today)
    sexo = forms.ChoiceField(widget=forms.Select(attrs={ 'class':"form-control",}),choices = usuario.Sexos, required = True)
    tlf = forms.CharField(widget=forms.TextInput(attrs={'type':"tel", 'class':"form-control",'id':"inputTelf", 'placeholder':"+0 123-4567891",}),validators=[phone_regex],label='Teléfono')
    correo = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'ejemplo@ejmpl.com','type':"email", 'class':"form-control", 'id':"inputEmail1", }))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'inputName' ,'placeholder':'usuario123',}),validators = [username_regex],max_length=40,label="Nombre de usuario")
    clave = forms.CharField(widget=forms.PasswordInput(attrs={'type':"password" ,'class':"form-control", 'id':"inputClave", 'placeholder':"Clave",}))
    
    