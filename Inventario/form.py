from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Permission
from Registro.models import ingrediente, ofrece, proveedor
from django.db import IntegrityError



class formIngredientes(forms.Form):
    ingredientes = forms.ModelChoiceField(queryset=ingrediente.objects.all().order_by('nombre'))

    def save(self):
        nombreIngr = self.cleaned_data['ingredientes']

        return ingrediente.objects.get(nombre = nombreIngr)

class formOfrece(forms.ModelForm):
    class Meta:
        model = ofrece
        exclude = ['usernameP','idIngr','idRest']

    def save(self,idIngr,usernameP):
        m = super(formOfrece, self).save(commit = False)
        m.idIngr = idIngr
        m.usernameP = usernameP
        
        query = ofrece.objects.filter(idIngr = idIngr, usernameP = usernameP)
        if query.exists():
           g = query[0]
           g.precio = m.precio
           m = g

        m.idRest = 1

        m.save()

        return m
