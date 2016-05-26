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

    platos = forms.MultipleChoiceField(choices = listaPlatos)



    def __init__(self, *args, **kwargs):
        super(platoSelector, self).__init__(*args, **kwargs)
        print('holis')
        print(args[0])

        self.fields['platos'].initial = [c.idItem for c in contiene.objects.filter(idMenu = args[0])]
