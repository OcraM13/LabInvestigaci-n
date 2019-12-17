from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import datos_usario
from .models import proyecto
from .models import integrantes_proyecto
from .models import registro
import random

def sesion_json(request,us,con):

    usuario = authenticate(username = us, password=con)

    if usuario is not None:

        do_login(request, usuario)

        generar_registro(request, usuarios.nombre + ' ' + usuarios.primer_ap + ' (' + usuarios.id_usuario + ') inicio Sesion desde la aplicacion', 0)

        return JsonResponse({'permisos':[{'permiso':'si'}]})
    else:
        return JsonResponse({'permisos':[{'permiso':'no'}]})

def proyectos_json(request):
    proyectos = proyecto.objects.values()

    lista = list(proyectos)

    return JsonResponse({'proyectos':lista})

from .models import proyecto

def proyectos_busca_json(request, bus):
    lista = []
    if bus != '-':
        proyectos = proyecto.objects.filter(Q(id_proyecto__icontains = str(bus))|Q(nombre_proyecto__icontains = str(bus)))
        proyectos_values = proyectos.values()
        lista = list(proyectos_values)
    else:
        proyectos = proyecto.objects.values()
        lista = list(proyectos)


    return JsonResponse({'proyectos':lista})

def agregar_proyecto_json(request,clase, nombre, nombre_sin, sin, por):

    try:
        num = ""

        comprobarcion = True

        while comprobarcion:
            num = generar_numero('P')

            if proyecto.objects.filter(id_proyecto = num):
                comprobarcion = True
            else:
                comprobarcion = False

        guardar_proyecto = proyecto(id_proyecto = num, clase= clase, nombre_proyecto= nombre, nombre_sin= nombre_sin, sintesis= sin, porsentaje= por)
        guardar_proyecto.save()

        usuarios = datos_usario.objects.get(usuario=str(request.user))

        if usuarios.id_usuario[0] == 'E':
            en = "Estudiante"
        else:
            en = "Asesor"

        us = usuarios.id_usuario

        integrantes = integrantes_proyecto(id_proyecto = num, id_usuario = us , encargo = en)

        integrantes.save()

    except Exception as e:

        return JsonResponse({'guardado':[{'estado':'no'}]})

    generar_registro(request, usuarios.nombre + ' ' + usuarios.primer_ap + ' (' + usuarios.id_usuario + ') Creo el proyecto ' + id + ' desde la aplicacion' , 0)

    return JsonResponse({'guardado':[{'estado':'si'}]})

def editar_proyecto_json(request, id, clase, nombre, nombre_sin, sin, por):

    try:

        guardar_proyecto = proyecto(id_proyecto = id, clase= clase, nombre_proyecto= nombre, nombre_sin= nombre_sin, sintesis= sin, porsentaje= por)
        guardar_proyecto.save()

    except Exception as e:

        return JsonResponse({'guardado':[{'estado':'no'}]})

    generar_registro(request, usuarios.nombre + ' ' + usuarios.primer_ap + ' (' + usuarios.id_usuario + ') Edito el proyecto ' + id + ' desde la aplicacion' , 0)

    return JsonResponse({'guardado':[{'estado':'si'}]})

def eliminar_proyecto_json(request, id):

    usuarios = datos_usario.objects.get(usuario=str(request.user))

    try:
        borrar = proyecto.objects.get(id_proyecto= id)
        borrar.delete()

        borrar = integrantes_proyecto.objects.filter(id_proyecto= id)
        borrar.delete()

    except Exception as e:
        return JsonResponse({'borrado':[{'estado':'no'}]})

    generar_registro(request, usuarios.nombre + ' ' + usuarios.primer_ap + ' (' + usuarios.id_usuario + ') elimino el proyecto ' + id + ' desde la aplicacion' , 0)

    return JsonResponse({'borrado':[{'estado':'si'}]})

# metodo generador interno ----------------------------------------------------------------------------------------------------------
def generar_numero(clase):
    hex = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D', 'E','F']
    num = clase + hex[random.randrange(15)] + hex[random.randrange(15)] + hex[random.randrange(15)] + hex[random.randrange(15)]
    return num

def generar_registro(request, mensaje, n):

    if n == 0:
        id = datos_usario.objects.get(usuario=str(request.user))
        usuario_str = id.nombre + " " + id.primer_ap + " (" + id.id_usuario + ") "
        nuevo_registro = registro(registro= usuario_str + mensaje)
        nuevo_registro.save()
    elif n == 1:
        usuario_str = str(request.user) + " "
        nuevo_registro = registro(registro= usuario_str + mensaje)
        nuevo_registro.save()
