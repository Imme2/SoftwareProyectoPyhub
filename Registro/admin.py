from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from Registro.models import perfil,menu,item,contiene,ingrediente, posee
from django.contrib.auth.models import User
# # Register your models here.
# admin.site.register(usuario)

'''
    Clases que permiten extender en el administrado de Django la clase User
'''

class perfilInline(admin.StackedInline):
    model = perfil
    can_delete = False
    verbose_name_plural = 'usuarios'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (perfilInline, )

'''
    Registro de modelos para poder ser editados desde el administrador de Django
'''
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(menu)
admin.site.register(item)
admin.site.register(contiene)
admin.site.register(ingrediente)
admin.site.register(posee)