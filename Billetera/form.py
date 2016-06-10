# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from Registro.models import billetera,transaccion
import datetime


def fechaVencimientoValidator(value):
    if value < datetime.date.today():
        raise ValidationError(
            ('La tarjeta ya esta vencida!'),
            params={'value': value},
        )

class formBilleteraRecargar(forms.Form):
    cardNum_regex = RegexValidator(regex=r'^([0-9]{4} ?){4}$', message="El numero de tarjeta debe tener el formato '1111 2222 3333 4444'")

    numeroTarjeta = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control", 'id':"inputCedula", 'placeholder':"1111 2222 3333 4444",}),validators=[cardNum_regex], label='Numero de Tarjeta')
    codigoSeguridad = forms.CharField(widget=forms.PasswordInput(attrs={'type':"password" ,'class':"form-control", 'id':"inputCodigoSeguridad", 'placeholder':"XXX",}),label = 'Codigo de Seguridad')
    clave = forms.CharField(widget=forms.PasswordInput(attrs={'type':"password" ,'class':"form-control", 'id':"inputClave", 'placeholder':"Clave",}),label = 'Clave')
    fechaVencimiento = forms.DateField(widget=forms.DateInput(attrs={'type':"date", 'class':"form-control", 'id':"inputF_Nac",}),label='Fecha de Vencimiento',validators= [fechaVencimientoValidator] ,initial=datetime.date.today)

    def save(self,request,monto):
        request.user.billetera.balance += monto
        request.user.billetera.save() 

class formTransaccion(forms.ModelForm):
    class Meta:
        model = transaccion
        exclude = ['idTrans','username','fecha']

    def save(self):
        m = super(formTransaccion, self).save(commit = False)
        return m.monto


class formBilleteraCrear(forms.Form):
    clave = forms.CharField(widget=forms.PasswordInput(attrs={'type':"password" ,'class':"form-control", 'id':"inputClave", 'placeholder':"Clave",}))
    repetirClave = forms.CharField(widget=forms.PasswordInput(attrs={'type':"password" ,'class':"form-control", 'id':"repeatInputClave", 'placeholder':"Repetir Clave",}))

    def clean(self):
        cleaned_data = super(formBilleteraCrear, self).clean()
        clave = cleaned_data.get('clave')
        repeticion = cleaned_data.get('repetirClave')

        if (clave != repeticion):
            msg = "Las claves deben ser iguales"
            self.add_error('repetirClave', msg)

        return cleaned_data

    def save(self,request):
        password = self.cleaned_data.get('clave')


        # Se crea la billetera con un password provicional
        b_entry = billetera.objects.create(user = request.user,password = 1)

        #Se setea correctamente el password de la billetera.
        b_entry.setPassword(password)

        #Se da el valor inicial del balance
        b_entry.balance = 0

        #se salva el objeto
        b_entry.save() 