from django.shortcuts import render
from django.http import HttpResponse
def index(request):
    return HttpResponse("<h2>Esta seraa la vista de registro de clientes.<h2>")