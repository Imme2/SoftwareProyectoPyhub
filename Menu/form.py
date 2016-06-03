# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Permission
from Registro.models import perfil, proveedor, menu,item,contiene
import datetime

class menuSelector(forms.Form):

    listaMenus = menu.objects.all()
    listaMenus = [x.nombre for x in listaMenus]

    
class formPlatoSelector(forms.Form):

    nombrePlato = forms.CharField(label = "Nombre de Menu:")
    platos = forms.ModelMultipleChoiceField(item.objects.all(), required=True, widget=forms.CheckboxSelectMultiple(), label='Selecciona los objetos del menu')

    def __init__(self, menuId = None, *args, **kwargs):
        super(formPlatoSelector, self).__init__(*args, **kwargs)
        if menuId:
            self.fields['platos'].initial = [c.idItem.idItem for c in contiene.objects.filter(idMenu = menuId)]
            self.fields['nombrePlato'].initial = menu.objects.get(idMenu = menuId).nombre

    def save(self, menuId):
        actual = [x.idItem for x in contiene.objects.filter(idMenu = menuId)]
        remover = [x for x in actual if x not in self.cleaned_data['platos']]
        agregar = [x for x in self.cleaned_data['platos'] if x not in actual]
        menuObj = menu.objects.get(idMenu = menuId)
        menuObj.nombre = self.cleaned_data['nombrePlato']
        menuObj.save()
        for x in agregar:
            contiene.objects.create(idMenu = menuObj, idItem = x)
        for x in remover:
            contiene.objects.filter(idMenu = menuObj, idItem = x).delete()
        return None

    def create(self):
        return menu.objects.create(nombre = self.cleaned_data['nombrePlato']).idMenu
