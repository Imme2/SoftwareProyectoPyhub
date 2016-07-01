from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Permission
from Registro.models import ingrediente, ofrece, proveedor
from django.db import IntegrityError

'''
 Formulario de ingredientes, que tiene una forma tipo "dropdown" de todos los
    ingredientes creados por el administrador del restaurante.
'''
class formIngredientes(forms.Form):
    ingredientes = forms.ModelChoiceField(queryset=ingrediente.objects.all().order_by('nombre'))

    def save(self):
        nombreIngr = self.cleaned_data['ingredientes']

        return ingrediente.objects.get(nombre = nombreIngr)


'''
 Ofrece los campos de precio de la relacion y guarda los resultados del campo.
    Ademas elimina la instancia de la relacion si el precio es menor que 0.
'''
class formOfrece(forms.ModelForm):
    class Meta:
        model = ofrece
        exclude = ['usernameP','idIngr','idRest']

    def save(self,idIngr,usernameP):
        m = super(formOfrece, self).save(commit = False)
        m.idIngr = idIngr
        m.usernameP = usernameP
        
        # Se verifica que no exista el objeto
        query = ofrece.objects.filter(idIngr = idIngr, usernameP = usernameP)

        #Si existe se debe editar
        if query.exists():
            g = query[0]
            if m.precio > 0:
                g.precio = m.precio
                m = g
            else:
                g.delete()
                return None

        if m.precio <= 0:
            return None

        m.idRest = 1

        m.save()

        return m
