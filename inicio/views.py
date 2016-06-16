from django.shortcuts import render
from django.http import HttpResponse
from inicio.controlador import getCurrentMenu

def index(request):
    menu = getCurrentMenu()
    return render(request,'inicio/home.html',{'menu': menu})