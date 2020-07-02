from django.shortcuts import render
from proyecto.views import lista_proyectos
from proyecto.models import lan_page
from django.http import HttpResponseRedirect

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return lista_proyectos(request)

    lan = lan_page.objects.filter(visible = '1')

    return render(request, 'inicio.html',{'landing':lan,'activo':lan[0].id})

def pag404(request, exception):
    return render(request, 'error404.html')

def login(request):
    return HttpResponseRedirect('/')
