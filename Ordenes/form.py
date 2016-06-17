# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from Registro.models import billetera,transaccion
import datetime

'''

 Formulario de pago con la billetera que pide la clave, la chequea, y genera la orden al
  pagar

'''
class formBilleteraPagar(forms.Form):

    clave = forms.CharField(widget=forms.PasswordInput(attrs={'type':"password" ,'class':"form-control", 'id':"inputClave", 'placeholder':"Clave",}),label = 'Clave de su Billetera:')
    monto = forms.DecimalField(label = 'Monto a pagar')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(formBilleteraRecargar, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(formBilleteraRecargar,self).clean()

        billeteraUsuario = self.request.user.billetera

        clave = cleaned_data.get('clave')

        if (not(billeteraUsuario.verifyPassword(clave))):
            msg = "Clave de billetera erronea."
            self.add_error('clave',msg)

        return cleaned_data

    def save(self,monto):

        self.request.user.billetera -= monto
        request.user.OrdenActual.tieneRel.clear()


        request.user.billetera.save() 