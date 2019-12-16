from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import datos_usario
from .models import proyecto

def sesion_json(request,us,con):

    usuario = authenticate(username = us, password=con)

    if usuario is not None:
        return JsonResponse({'permiso':{'permiso':'si'}})
    else:
        return JsonResponse({'permiso':{'permiso':'no'}})



def proyectos_json(request):
    proyectos = proyecto.objects.values()

    lista = list(proyectos)

    return JsonResponse({'proyectos':lista})
