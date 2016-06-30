# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from Registro.models import billetera, transaccion, orden, tieneActual, tiene, posee, ingrediente, resena, ofrece, egreso
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
        platos = tieneActual.objects.filter(orden = user.ordenActual)
        errores = ingredientesPedido(user)
        if not (errores):

            user.billetera.balance -= monto
            user.billetera.save() 

            nuevaOrden = orden(user = user)
            nuevaOrden.fecha = datetime.datetime.today()
            nuevaOrden.totalPagado = monto
            nuevaOrden.save()

            for x in platos:
                tiene.objects.create(orden = nuevaOrden, item = x.item, cantidad = x.cantidad)            
            nuevaOrden.save()

            user.ordenActual.tieneRel.clear()
            user.ordenActual.save()
            return ['valid',nuevaOrden]

        else:
            return ['error',errores]


class formResena(forms.ModelForm):

    activarResena = forms.BooleanField(required = False) 

    class Meta:
        model = resena
        fields = ['contenido']
    
    def __init__(self, *args, **kwargs):
        super(formResena, self).__init__(*args, **kwargs)
        self.fields['activarResena'].label = "Dejar Reseña"
        self.fields['contenido'].label = "Reseña"
        self.fields['contenido'].required = False
        self.fields['contenido'].widget.attrs.update({"class":"form-control"})


    def save(self,orden):
        if self.cleaned_data['activarResena']:
            contenido = self.cleaned_data['contenido']
            if contenido is not '':
                entry = resena.objects.create(orden = orden, contenido = contenido)
                entry.save()

class formOferta(forms.Form):

    id_ofrece = forms.IntegerField(widget=forms.HiddenInput())
    cantidad = forms.IntegerField(min_value=0) 

    def save(self):
        oferta = ofrece.objects.get(pk = self.cleaned_data['id_ofrece'])
        oferta.idIngr.cantidad += self.cleaned_data['cantidad']
        oferta.idIngr.save()
        e = egreso(username = oferta.usernameP.username, 
            monto = -(self.cleaned_data['cantidad'] * oferta.precio), 
            fecha = datetime.datetime.today())
        e.save()

def ingredientesPedido(user):
    tiene = tieneActual.objects.filter(orden = user.ordenActual)
    errores = []
    salvar = []
    fullfill = True
    for objeto in tiene:
        ingredientes = posee.objects.filter(idItem = objeto.item)
        for x in ingredientes:
            ingr = x.idIngr
            descontar = objeto.cantidad * x.cantidad
            if ingr.cantidad >= descontar:
                ingr.cantidad -= descontar
            else: 
                errores.append(ingr.nombre)
                fullfill = False
            salvar.append(ingr)

    if fullfill:
        for x in salvar:
            x.save()
        return False
    else:
        print(errores)
        return errores


