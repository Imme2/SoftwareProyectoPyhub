# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from Registro.models import billetera,transaccion,orden,tieneActual,tiene
import datetime

'''

 Formulario de pago con la billetera que pide la clave, la chequea, y genera la orden al
  pagar

'''
class formBilleteraPagar(forms.Form):

    clave = forms.CharField(widget=forms.PasswordInput(attrs={'type':"password" ,'class':"form-control", 'id':"inputClave", 'placeholder':"Clave",}),label = 'Clave de su Billetera:')
    monto = forms.DecimalField(label = 'Monto a pagar') 

    def __init__(self,monto = 0, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(formBilleteraPagar, self).__init__(*args, **kwargs)
        self.fields['monto'].initial = monto
        self.fields['monto'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super(formBilleteraPagar,self).clean()

        billeteraUsuario = self.request.user.billetera

        clave = cleaned_data.get('clave')

        if (not(billeteraUsuario.verifyPassword(clave))):
            msg = "Clave de billetera erronea."
            self.add_error('clave',msg)

        monto = cleaned_data.get('monto')
        if(monto > self.request.user.billetera.balance):
            msg = "No tiene suficiente saldo."
            self.add_error('monto',msg)
            
        if(monto == 0):
            msg = "Debe comprar algo."
            self.add_error('monto',msg)
        return cleaned_data

    def save(self):
        monto = self.cleaned_data.get('monto')

        user = self.request.user

        user.billetera.balance -= monto
        user.billetera.save() 

        platos = tieneActual.objects.filter(orden = user.ordenActual)
        
        nuevaOrden = orden(user = user)
        nuevaOrden.fecha = datetime.datetime.today()
        nuevaOrden.totalPagado = monto
        nuevaOrden.save()
        
        for x in platos:
            tiene.objects.create(orden = nuevaOrden, item = x.item, cantidad = x.cantidad)            
        nuevaOrden.save()

        user.ordenActual.tieneRel.clear()
        user.ordenActual.save()
