# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Permission
from Registro.models import item, ordenActual



class formMostrarPlato(forms.ModelForm):

    cantidad = forms.IntegerField(widget=forms.NumberInput(attrs={'class':"form-control"}),min_value = 0,required = True, initial = 0)


    def __init__(self, *args, **kwargs):
        super(formMostrarPlato, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['readonly'] = True
        self.fields['precio'].widget.attrs['readonly'] = True
        self.fields['descripcion'].widget.attrs['readonly'] = True

    class Meta:
        model = item
        exclude = ('idItem','tipo','poseeRel','foto',)


    def save(self,request):
        try:
            orden = request.user.ordenActual
        except:
            orden = ordenActual.objects.create(user = request.user)
        plato = super(formMostrarPlato,self).save(commit=False)
        N = self.cleaned_data.get('cantidad')
        while(N > 0):
            orden.tieneRel.add(plato)
            N -= 1

        orden.save()


'''
class formMostrarMenu(forms.Form):

    platos = forms.ModelMultipleChoiceField(contiene.objects.filter(idMenu = self.menuId), required=True, widget=forms.CheckboxSelectMultiple(attrs={'type':"checkbox",}), label='Selecciona los objetos del menu')

    def __init__(self, menuId = None, *args, **kwargs):
        self.menuId = kwargs.pop('menuId', None)
        super(formMenu, self).__init__(*args, **kwargs)

    def save(self, menuId):

        for x in agregar:
            contiene.objects.create(idMenu = menuObj, idItem = x)
        for x in remover:
            contiene.objects.filter(idMenu = menuObj, idItem = x).delete()
        return None

    def create(self):
        return menu.objects.create(nombre = self.cleaned_data['nombreMenu']).idMenu
'''