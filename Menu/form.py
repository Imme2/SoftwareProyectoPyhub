# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Permission
from Registro.models import ingrediente, perfil, proveedor, menu, item,contiene,posee
from django.db import IntegrityError
import datetime
import pickle


class formMenu(forms.Form):

    nombreMenu = forms.CharField(widget=forms.TextInput(attrs={'type':'text' ,'class':'form-control' ,'id':'inputNombreMenu', 'placeholder':'Nombre Menu',}),label = "Nombre de Menu:")
    platos = forms.ModelMultipleChoiceField(item.objects.all(), required=True, widget=forms.CheckboxSelectMultiple(), label='Selecciona los objetos del menu')

    def __init__(self, menuId = None, *args, **kwargs):
        super(formMenu, self).__init__(*args, **kwargs)
        if menuId:
            self.fields['platos'].initial = [c.idItem.idItem for c in contiene.objects.filter(idMenu = menuId)]
            self.fields['nombreMenu'].initial = menu.objects.get(idMenu = menuId).nombre

    def save(self, menuId):
        actual = [x.idItem for x in contiene.objects.filter(idMenu = menuId)]
        remover = [x for x in actual if x not in self.cleaned_data['platos']]
        agregar = [x for x in self.cleaned_data['platos'] if x not in actual]
        menuObj = menu.objects.get(idMenu = menuId)
        menuObj.nombre = self.cleaned_data['nombreMenu']
        menuObj.saves()
        for x in agregar:
            contiene.objects.create(idMenu = menuObj, idItem = x)
        for x in remover:
            contiene.objects.filter(idMenu = menuObj, idItem = x).delete()
        return None

    def create(self):
        return menu.objects.create(nombre = self.cleaned_data['nombreMenu']).idMenu


class ingredienteForm(forms.ModelForm):
    class Meta:
        model = ingrediente
        exclude = ['idIngr']

class formPlato(forms.ModelForm):
    class Meta:
        model = item
        exclude = ['idItem','poseeRel']

class formPosee(forms.ModelForm):
    class Meta:
        model = posee
        exclude = ['idItem']

    def save(self,idItem):
        m = super(formPosee, self).save(commit = False)
        m.idItem = idItem
        query = posee.objects.filter(idItem = m.idItem, idIngr = m.idIngr)
        if query.exists():
            g = query[0]
            g.cantidad = m.cantidad
            g.save()
            return g
        else: 
            m.save()
            return m