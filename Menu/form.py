# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Permission
from Registro.models import perfil, proveedor, menu,item,contiene
import datetime

class menuCrear(forms.Form):

    idMenu = forms.DecimalField(min_value = 0, label = "Id del menu")
    nombreMenu = forms.CharField(max_length= 50, label = "Nombre del Menu")

    def clean(self):
        cleaned_data = super(menuCrear, self).clean()
        idMenu = cleaned_data.get('idMenu')
        nombreMenu = cleaned_data.get('nombreMenu')

        if menu.objects.filter(nombre = nombreMenu).exists():
            msg = "El nombre del menu ya existe"
            self.add_error('nombreMenu', msg)
            
        if menu.objects.filter(idMenu = idMenu).exists():
            msg = "El id del menu ya existe"
            self.add_error('idMenu', msg)

        return cleaned_data

    def save(self):
        idMenu = self.cleaned_data['username']
        nombreMenu = self.cleaned_data['nombre']
        menuEntry = menu.objects.create(idMenu = idMenu)
        menuEntry.nombre = nombreMenu
        menuEntry.save()
        return menuEntry



class menuSelector(forms.Form):

    listaMenus = menu.objects.all()
    listaMenus = [x.nombre for x in listaMenus]

#    menus = forms.choiceField(choices = listaMenus)
    
class platoSelector(forms.Form):

    listaPlatos = item.objects.all()
    listaPlatos = [(x.idItem,x.nombre) for x in listaPlatos]

    #platos = forms.MultipleChoiceField(choices = listaPlatos)
    nombrePlato = forms.CharField(label = "Nombre del plato")
    platos = forms.ModelMultipleChoiceField(item.objects.all(), required=True, widget=forms.CheckboxSelectMultiple(), label='Selecciona los objetos del menu')
    #platos = forms.ChoiceField(widget=forms.CheckboxSelectMultiple,choices = item.objects.all())

    def __init__(self, menuId, *args, **kwargs):
        super(platoSelector, self).__init__(*args, **kwargs)
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