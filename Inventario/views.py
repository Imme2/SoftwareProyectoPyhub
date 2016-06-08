from django.shortcuts import render
from Registro.views import esProveedor
# Create your views here.


@login_required(login_url='/registro/login/')
def crearInventario(request):
    if (not(esProveedor(request))):
        return HttpResponseRedirect('')
    if (idMenu == None):
        listaMenus = menu.objects.all()
        return render(request,'menu/escoger.html', {'listaMenu': listaMenus})
    else:
        if request.method == "POST":
            formPlatos = formMenu(idMenu, data = request.POST)
            if formPlatos.is_valid():
                formPlatos.save(idMenu)
                return HttpResponseRedirect('/menu/editar/{}'.format(idMenu))
            else :
                print(formPlatos.data)
                return HttpResponseRedirect('/menu/editar/{}'.format(idMenu))                
        else:
            nombreMenu = menu.objects.get(idMenu = idMenu).nombre
            formPlatos = formMenu(idMenu)

            return render(request,'menu/editar.html', {'nombreMenu': "Editar un menu",
                                                    'form': formPlatos})

def modificarInventario(request):
    pass