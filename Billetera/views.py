from django.shortcuts import render

# Create your views here.


@login_required(login_url='/registro/login/')
def crearBilletera(request):
    #Check de si tiene una billetera ya.
    try:
        request.user.billetera
        return HttpResponseRedirect('Billetera/recargar')
    except:
        pass
    if request.method == "POST":
        form = billeteraAuth(request.POST)
        if form.is_valid():
            form.save(request)
            return HttpResponseRedirect('Billetera/recargar')
        else:
            return render(request,'billetera/crear.html', {'form': form})
    else:
        form = billeteraAuth()
        return render(request,'billetera/crear.html', {'form': form})

def recargarBilletera(request):
    pass