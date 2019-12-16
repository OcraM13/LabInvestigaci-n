from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import inicio
from .views import ejemplo
from .views import crear_proyecto
from .views import crear_cuenta
from .views import nuevo_pdf
from .views import nuevo_miembro
from .views import lista_proyectos
from .views import editar_proyecto
from .views import Sesion
from .views import salirUsuario
from .views import crear_usuario_oficial
from .views import pag_proyecto
from .views import borrar_integrante
from .views import lista_sintesis
from .views import editar_usuario
from .views import comentarios
from .views import lista_registros
from .views_json import proyectos_json
from .views_json import sesion_json
#from .views import sesion

urlpatterns = [
    path('',inicio, name = 'inicio'),
    path('ejemplo/', ejemplo, name = 'ejemplo'),
    path('crear_proyecto/', login_required(crear_proyecto), name='crear_proyecto'),
    path('nuevo_usuario/', login_required(crear_cuenta), name='crear_cuenta'),
    path('subir_pdf/<id>', login_required(nuevo_pdf), name='nuevo_pdf'),
    path('integrantes/<id>', login_required(nuevo_miembro), name='nuevo_miembro'),
    path('lista_proyectos/', login_required(lista_proyectos), name='lista_proyectos'),
    path('editar_proyecto/<id>', login_required(editar_proyecto), name="editar_proyecto"),
    path('sesion/', Sesion.as_view(), name='sesion'),
    #path('sesion', sesion, name='Sesion'),
    path('salir/', login_required(salirUsuario), name='salir'),
    path('crear_usuario/', login_required(crear_usuario_oficial), name='crear_usuario'),
    path('proyecto/<id>', login_required(pag_proyecto), name='pag_proyecto'),
    path('borrar_int/<id>/<us>', login_required(borrar_integrante), name='borrar_int'),
    path('lista_sintesis/', lista_sintesis, name='lista_sin'),
    path('editar_usuario/', login_required(editar_usuario), name='editar_usuario'),
    path('comentarios/<id>', login_required(comentarios), name='comentarios' ),
    path('registros/', login_required(lista_registros), name='registros' ),
    path('proyectos_json/', proyectos_json, name='proyectos_json'),
    path('sesion_json/<us>/<con>', sesion_json, name='sesion_json'),
]
