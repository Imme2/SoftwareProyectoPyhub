# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from Registro.models import billetera


class billeteraAuth(forms.Form):
    clave = forms.CharField(widget=forms.PasswordInput(attrs={'type':"password" ,'class':"form-control", 'id':"inputClave", 'placeholder':"Clave",}))
    repetirClave = forms.CharField(widget=forms.PasswordInput(attrs={'type':"password" ,'class':"form-control", 'id':"repeatInputClave", 'placeholder':"Repetir Clave",}))

    def clean(self):
        cleaned_data = super(billeteraAuth, self).clean()
        clave = cleaned_data.get('clave')
        repeticion = cleaned_data.get('repetirClave')

        if (clave != repeticion):
            msg = "Las claves deben ser iguales"
            self.add_error('repetirClave', msg)

        return cleaned_data

    def save(self,request):
        password = self.cleaned_data('clave')

        b_entry = request.user.billetera
         