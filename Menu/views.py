from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from Registro.models import perfil,proveedor
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/registro/login/')
def cambiarMenu(request):
	if (not(request.user.has_perm('admin'))):
		return HttpResponseRedirect(request,''):

	