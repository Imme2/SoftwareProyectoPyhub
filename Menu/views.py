from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from Registro.models import perfil,proveedor
from django.contrib.auth.decorators import login_required
from Menu.form import "FORMS"
# Create your views here.


@login_required(login_url='/registro/login/')
def crearMenu(request):
	if (not(request.user.has_perm('admin'))):
		return HttpResponseRedirect(request,''):

	if request.method == "POST":


		
	else:



@login_required(login_url='/registro/login/')
def cambiarMenu(request):
	if (not(request.user.has_perm('admin'))):
		return HttpResponseRedirect(request,''):

	if request.method == "POST":



	else:


def cambiarMenuEsp(request):