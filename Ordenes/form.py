# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from Registro.models import billetera,transaccion,orden
import datetime

'''

 Formulario de pago con la billetera que pide la clave, la chequea, y genera la orden al
  pagar

'''
class formBilleteraPagar(forms.Form):

    clave = forms.CharField(widget=forms.PasswordInput(attrs={'type':"password" ,'class':"form-control", 'id':"inputClave", 'placeholder':"Clave",}),label = 'Clave de su Billetera:')
    monto = forms.DecimalField(label = 'Monto a pagar',disabled = True) 

    def __init__(self,monto = 0, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(formBilleteraPagar, self).__init__(*args, **kwargs)
        self.fields['monto'].initial = monto

    def clean(self):
        cleaned_data = super(formBilleteraPagar,self).clean()

        billeteraUsuario = self.request.user.billetera

        clave = cleaned_data.get('clave')

        if (not(billeteraUsuario.verifyPassword(clave))):
            msg = "Clave de billetera erronea."
            self.add_error('clave',msg)

        return cleaned_data

    def save(self):
        monto = self.cleaned_data.get('monto')

        user = self.request.user

        user.billetera -= monto
        user.billetera.save() 

        platos = user.ordenActual.tieneRel.all()
        
        nuevaOrden = orden.objects.create(user = user)
        nuevaOrden.fecha = datetime.today()
        nuevaOrden.totalPagado = monto
        for x in platos:
            nuevaOrden.tieneRel.add(X)
        nuevaOrden.save()

        user.ordenActual.tieneRel.clear()
        user.ordenActual.save()
