# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from Registro.models import perfil, proveedor, parametro
import datetime

'''
    Funcion que permite validar las fechas
'''

def dateValidator(value):
    if value > datetime.date.today():
        raise ValidationError(
            ('La fecha de Nacimiento no puede ser en el futuro!'),
            params={'value': value},
        )

'''
    Forma para registrar usuarios.
'''

class formRegistroUsuario(forms.Form):
    phone_regex = RegexValidator(regex=r'^\+?(58)?\d{11,14}$', message="El numero de telefono debe tener el formato: '+5899999999999'.")
    ci_regex = RegexValidator(regex=r'^[VP]\d{8}$', message="La Cedula debe tener el formato 'V50123456'")
    username_regex = RegexValidator(regex = r'^([A-Za-z]|\d|\.|\_)*$',message = "Tu Username solo puede contener caracteres alphanumericos, puntos (.) o pisos (_). No se aceptan espacios.")
    nombres_regex = RegexValidator(regex = r'^[A-Za-z]{4,41}$', message = "Un Nombre solo puede contener letras del alfabeto")
    apellidos_regex = RegexValidator(regex = r"^[A-Z'a-z]+( [A-Z'a-z]+)*$", message = "Un Apellido solo puede contener nombres del alfabeto y apostrofes (').")

    nombre = forms.CharField(widget=forms.TextInput(attrs={'type':'text' ,'class':'form-control' ,'id':'inputName', 'placeholder':'Fulano',}),validators = [nombres_regex], max_length=100)
    apellidos = forms.CharField(widget=forms.TextInput(attrs={'type':'text' ,'class':'form-control' ,'id':'inputApellido', 'placeholder':'Detal',}),validators = [apellidos_regex], max_length=100)
    ci = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control", 'id':"inputCedula", 'placeholder':"V123456789",}),validators=[ci_regex], label='Cédula')
    f_nac = forms.DateField(widget=forms.DateInput(attrs={'type':"date", 'class':"form-control", 'id':"inputF_Nac",}),label='Fecha de Nacimiento',validators= [dateValidator] ,initial=datetime.date.today)
    sexo = forms.ChoiceField(widget=forms.Select(attrs={ 'class':"form-control",}),choices = perfil.Sexos, required = True)
    tlf = forms.CharField(widget=forms.TextInput(attrs={'type':"tel", 'class':"form-control",'id':"inputTelf", 'placeholder':"+0 123-4567891",}),validators=[phone_regex],label='Teléfono',required=False)
    correo = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'ejemplo@ejmpl.com','type':"email", 'class':"form-control", 'id':"inputEmail1", }))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'inputName' ,'placeholder':'usuario123',}),validators = [username_regex],max_length=40,label="Nombre de usuario")
    clave = forms.CharField(widget=forms.PasswordInput(attrs={'type':"password" ,'class':"form-control", 'id':"inputClave", 'placeholder':"Clave",}))

    def clean(self):
        cleaned_data = super(formRegistroUsuario, self).clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        ci = cleaned_data.get('ci')

        if User.objects.filter(username=username).exists():
            msg = "El nombre de usuario ya esta utilizado"
            self.add_error('username', msg)
            
        if User.objects.filter(email=email).exists():
            msg = "El correo ya esta utilizado"
            self.add_error('correo', msg)
    
        if perfil.objects.filter(ci=ci).exists():
            msg = "Esta CI ya esta registrada"
            self.add_error('ci', msg)
            
        return cleaned_data
    
    def save(self):

        username = self.cleaned_data['username']
        nombre = self.cleaned_data['nombre']
        apellidos = self.cleaned_data['apellidos']
        fechaNac = self.cleaned_data['f_nac']
        correo = self.cleaned_data['correo']
        tlf = self.cleaned_data['tlf']
        clave = self.cleaned_data['clave']
        sexo = self.cleaned_data['sexo']
        ci = self.cleaned_data['ci']
        entry = User.objects.create_user(username= username ,email = correo, password = clave)
        entry.first_name = nombre
        entry.last_name = apellidos
        entry.save()
        p_entry = entry.perfil
        p_entry.ci = ci
        p_entry.sexo = sexo
        p_entry.fechaNac = fechaNac
        p_entry.tlf = tlf
        p_entry.save()
        return entry
        
'''
    Forma para registrar proveedores.
'''

class formRegistroProveedor(forms.Form):
    rif_regex = RegexValidator(regex=r'^[A-Z][0-9]{6,8}$', message="El RIF debe ser de la forma A12311231.")

    rif = forms.CharField(widget=forms.TextInput(attrs={'type':'text' ,'class':'form-control' ,'id':'inputRif', 'placeholder':'J1234560',}),validators = [rif_regex], label ='RIF', max_length = 20)
    nombreEmpresa = forms.CharField(widget=forms.TextInput(attrs={'type':'text' ,'class':'form-control' ,'id':'inputNombreEmpresa', 'placeholder':'Platanitos Rosa .Inc',}),validators = [],label = 'Nombre de la Empresa', max_length = 40)

    def clean(self):
        cleaned_data = super(formRegistroProveedor, self).clean()
        rif = cleaned_data.get('rif')
        nombreEmpresa = cleaned_data.get('nombreEmpresa')

        if proveedor.objects.filter(rif=rif).exists():
            msg = "Este rif ya esta registrado."
            self.add_error('rif', msg)
            
        if proveedor.objects.filter(nombreEmpr=nombreEmpresa).exists():
            msg = "Este nombre de empresa ya esta registrado."
            self.add_error('nombreEmpresa', msg)
    
        return cleaned_data

    def save(self,request,entry):
#        m = super(formRegistroProveedor, self).save(commit = False)
        rif = self.cleaned_data['rif']
        nombreEmpr = self.cleaned_data['nombreEmpresa']
        
        #   entry cableado para que se salve como el foreign key bien.

        prov_entry = proveedor.objects.create(username = entry)
        prov_entry.rif = rif
        prov_entry.nombreEmpr = nombreEmpr
 
        prov_entry.save()

        # Le agregamos un permiso que nos diga que es proveedor.
        #Cambiar a grupos un dia que no sea 3 am.
        try:
            permission = Permission.objects.get(codename='proveedor')
        except:
            content_type = ContentType.objects.get(model='user')
            Permission.objects.create(codename='proveedor',
                                       name='es proveedor',
                                        content_type = content_type)
            permission = Permission.objects.get(codename='proveedor')

        print(permission)
        a = User.objects.get(username= entry.username)
        a.user_permissions.add(permission)
        a.save()


#        return m
'''
    Forma para identificar a los usuarios
'''

class loginUsuario(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'type':'text' ,'class':'form-control' ,'id':'inputNombreUs', 'placeholder':'usuario123',}),label='Nombre de usuario', max_length=40)
    clave = forms.CharField(widget=forms.PasswordInput(attrs={'type':"password" ,'class':"form-control", 'id':"inputClave", 'placeholder':"Clave",}))
    

'''
    Forma para modificar los parametros del restaurante.
'''

class parametrosForm(forms.ModelForm):

    class Meta:
        model = parametro
        exclude = ('idParam', )

    def __init__(self, *args, **kwargs):
        super(parametrosForm, self).__init__(*args, **kwargs)
        self.fields['menuActual'].widget.attrs.update({'class':'form-control'})
        self.fields['horarioCierre'].widget.attrs.update({'class':'form-control'})
        self.fields['horarioEntrada'].widget.attrs.update({'class':'form-control'})
        self.fields['cantPuestos'].widget.attrs.update({'class':'form-control'})

'''
    Formulario para cambiar la clave de un usuario.
'''

class formCambiarClave(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={'type':"password" ,'class':"form-control", 'id':"inputClave", 'placeholder':"Clave Actual",}))
    nuevaClave = forms.CharField(widget=forms.PasswordInput(attrs={'type':"password" ,'class':"form-control", 'id':"inputClave", 'placeholder':"Nueva Clave",}))
    repetirClave = forms.CharField(widget=forms.PasswordInput(attrs={'type':"password" ,'class':"form-control", 'id':"repeatInputClave", 'placeholder':"Repetir Nueva Clave",}))
    class Meta:
        model = User
        fields = ['password']

    def clean(self):
        cleaned_data = super(formCambiarClave, self).clean()
        clave = cleaned_data.get('nuevaClave')
        repeticion = cleaned_data.get('repetirClave')
        claveActual = cleaned_data.get('password')

        usuario = self.instance

        if (clave != repeticion):
            msg = "Las claves deben ser iguales"
            self.add_error('repetirClave', msg)

        if not usuario.check_password(claveActual):
            msg = "Clave incorrecta."
            self.add_error('password',msg)

        return cleaned_data

    def save(self):
        m = super(formCambiarClave, self).save(commit = False)

        clave = self.cleaned_data.get('nuevaClave')

        #Se setea correctamente el password de la billetera.
        m.set_password(clave)

        m.save()


'''
    ##############################
    
    Formas para mostrar, con campos deshabilitados.

    ##############################
'''


'''
    Forma para mostrar al usuario.
'''

class userForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'inputName',}),disabled = True, label = 'Nombre de usuario')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'type':'text' ,'class':'form-control' ,'id':'inputName',}),disabled = True, label = 'Nombre')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'type':'text' ,'class':'form-control' ,'id':'inputApellido',}),disabled = True, label = 'Apellido')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'ejemplo@ejmpl.com','type':"email", 'class':"form-control", 'id':"inputEmail1", }),disabled = True, label = 'Correo')
#    password = forms.CharField(widget=forms.PasswordInput(attrs={'type':"password" ,'class':"form-control", 'id':"inputClave", 'placeholder':"Clave",}), label = 'Contrasena', required = False)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        
   
'''
    Forma para mostrar el perfil del usuario.
'''

class perfilForm(forms.ModelForm):
    fechaNac = forms.DateField(widget=forms.TextInput(attrs={'type':"tel", 'class':"form-control",'id':"inputTelf",}),disabled = True, label = 'Fecha de nacimiento')
    tlf = forms.CharField(widget=forms.TextInput(attrs={'type':"tel", 'class':"form-control",'id':"inputTelf",}),label = 'Numero de telefono')
    ci = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control", 'id':"inputCedula",}),disabled = True, label = 'CI')
    sexo = forms.ChoiceField(widget=forms.Select(attrs={ 'class':"form-control",}),choices = perfil.Sexos, disabled = True)
#    foto = forms.CharField(widget=forms.TextInput(attrs={'type':"text", 'class':"form-control",'id':"inputTelf",}),label = 'Foto')


    class Meta:
        model = perfil
        exclude = ('user',) 

#    def save(self,request):
#        m = super(perfilForm, self).save(commit = False)
#        m.user = request.user
#        m.save()
#        return m

'''
    Forma de proveedor para mostrar en el perfil, donde los campos estan deshabilitados.
'''

class proveedorForm(forms.ModelForm):
    nombreEmpr = forms.CharField(widget=forms.TextInput(attrs={'type':'text' ,'class':'form-control' ,'id':'inputNombreEmpresa',}),disabled = True, label = 'Nombre de Empresa')
    rif = forms.CharField(widget=forms.TextInput(attrs={'type':'text' ,'class':'form-control' ,'id':'inputRif',}),disabled = True, label = 'RIF')
    class Meta:
        model = proveedor
        exclude = ('username','ofreceRel')

    def save(self,request):
        m = super(proveedorForm, self).save(commit = False)
        m.username = request.user
        m.save()
        return m
