from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import SesionForm
from .forms import ProyectoForm
from .forms import UsuarioForm
from .forms import CuentaForm
from .forms import PdfForm
from .forms import MiembroFrom
from .forms import RegistroFrom
from .forms import ComentarioFrom
from .models import usuario
from .models import proyecto
from .models import integrantes_proyecto
from .models import comentario
from .models import datos_usario
from .models import pdf
from .models import registro
from .filters import ProyectosFiltros
from .filters import RegistroFiltros
import random

# Create your views here.

def inicio(request):
    return render(request, 'inicio.html')

def ejemplo(request):
    return render(request, 'ejemplo.html')

# crear proyecto ------------------------------------------------------------------------------------------------------------

def crear_proyecto(request):
    if request.method == 'POST':
        proyecto_form = ProyectoForm(request.POST)
        print(proyecto_form)
        if proyecto_form.is_valid():
            print("----------------------------------------------------------------")

            post = proyecto_form.save(commit=False)

            num = generar_numero('P')
            post.id_proyecto = num

            post.save()
            generar_registro(request, 'creo proyecto ' + num, 0)
            return HttpResponseRedirect('/Lab/integrantes/'+post.id_proyecto)

    else:
        proyecto_form = ProyectoForm()

    return render(request, 'crear_proyecto.html',{'proyectos':'ID','acto':'Crear Proyecto','id':'ID'})

# crear cuenta ---------------------------------------------------------------------------------------------------------------

def crear_cuenta(request):
    if request.method == 'POST':
        post_usuario = UsuarioForm(request.POST)

        if post_usuario.is_valid():

            num = ""

            post_u = post_usuario.save(commit=False)

            if post_u.tipo == '1':
                num = generar_numero('E')
            else:
                num = generar_numero('D')

            cuenta = User.objects.create(username=num)

            cuenta.set_password('1234')

            cuenta.save()
            generar_registro(request, 'creo cuenta temporal ' + num, 0)
            messages.info(request, 'Nueva Cuenta: ' + num)

            return redirect('proyecto:crear_cuenta')

    else:
        cuenta_form = UsuarioForm()

    return render(request, 'crear_usuario.html')

# crear usuario-----------------------------------------------------------------------------------------------------------------

def crear_usuario_oficial(request):

    usuario = str(request.user)

    tipo =""

    if usuario[0] == 'D':
        tipo='0'
    else:
        tipo='1'

    if request.method == 'POST':
        usuarios_form = UserCreationForm(request.POST)
        datos_form = UsuarioForm(request.POST)

        if datos_form.is_valid():

            if usuarios_form.is_valid():

                post_datos = datos_form.save(commit=False)
                post_u = usuarios_form.save(commit=False)

                post_datos.usuario = post_u.username
                post_datos.id_usuario = usuario

                post_u.save()
                post_datos.save()
                generar_registro(request, 'fue registrado', 1)

                if usuario != 'marco':
                    u = User.objects.get(username = usuario)
                    u.delete()

                return HttpResponseRedirect('/Lab')

    else:
        usuarios_form = UserCreationForm()
        datos_form = UsuarioForm()

    return render(request,'editar_usuario.html',{'usuario':usuario, 'cero':0, 'tipo':tipo, 'form':usuarios_form})

# subur pdf ------------------------------------------------------------------------------------------------------------------------

def nuevo_pdf(request, id):
    if request.method == 'POST':

        pdf_form = PdfForm(request.POST)

        if pdf_form.is_valid():

            pdf_form.save()

            generar_registro(request, 'subio pdf al pryecto' + id, 0)

            return HttpResponseRedirect('/Lab/proyecto/'+id)

    else:
        pdf_form = PdfForm()
        print(pdf_form)

    return render(request, 'nuevo_pdf.html', {'id':id})

# nuevo miembro --------------------------------------------------------------------------------------------------------------------

def nuevo_miembro(request, id):
    if request.method == 'POST':

        miembro_form = MiembroFrom(request.POST)


        if miembro_form.is_valid():
            post = miembro_form.save()
            generar_registro(request, 'agreo a ' + str(post.id_usuario.id_usuario) +' al proyecto ' + id, 0)
            return HttpResponseRedirect('/Lab/integrantes/'+id)

    else:
        miembro_form = MiembroFrom()

    us = datos_usario.objects.get(usuario = str(request.user))
    integrantes = integrantes_proyecto.objects.filter(id_proyecto = id)
    usuarios = datos_usario.objects.all

    return render(request, 'nuevo_miembro.html', {'id':id,'us':'Us Id '+us.id_usuario, 'integrantes':integrantes, 'usuarios':usuarios})

# comentarios ------------------------------------------------------------------------------------------------------------------

def comentarios(request,id):

    id_us = datos_usario.objects.get(usuario=str(request.user))
    comentarios = comentario.objects.filter(id_pdf=id)
    pdf_con = pdf.objects.get(id_pdf = id)
    usuarios = datos_usario.objects.all

    if request.method == 'POST':
        comentario_from = ComentarioFrom(request.POST)
        if comentario_from.is_valid():
            comentario_from.save()
            generar_registro(request, 'comento en el pdf "' + pdf_con.pdf_nombre + '" del proyecto ' + pdf_con.id_proyecto.id_proyecto, 0)
            return HttpResponseRedirect('/Lab/comentarios/'+id)
    comentario_from = ComentarioFrom()
    print(comentario_from)

    return render(request, 'comentarios.html',{'us':id_us,'id':id, 'comentarios':comentarios, 'usuarios':usuarios})

# lista Proyectos ------------------------------------------------------------------------------------------------------------------

def lista_proyectos(request):

    if not datos_usario.objects.filter(usuario=str(request.user)):
        return HttpResponseRedirect('/Lab/crear_usuario')

    id = datos_usario.objects.get(usuario=str(request.user))

    usuario = integrantes_proyecto.objects.filter(id_usuario=id.id_usuario)

    filtro = request.GET.get('filtro')

    if not filtro == None:
        proyectos = proyecto.objects.filter(Q(id_proyecto__icontains = str(filtro))|Q(nombre_proyecto__icontains = str(filtro)))
        return render(request, 'lista_proyectos.html', {'proyectos':proyectos,'usuario':usuario, 'id':id.id_usuario, 'admin':'E0001'})

    proyectos = proyecto.objects.all

    return render(request, 'lista_proyectos.html', {'proyectos':proyectos,'usuario':usuario, 'id':id.id_usuario, 'admin':'E0001'})

# lista Sintesis ------------------------------------------------------------------------------------------------------------------

def lista_sintesis(request):

    proyectos = proyecto.objects.all

    return render(request, 'lista_sin.html', {'proyectos':proyectos})

# lista Sintesis ------------------------------------------------------------------------------------------------------------------

def lista_registros(request):

    if not User.is_authenticated:
        return render(request, 'lista_proyectos')

    filtro = request.GET.get('filtro')

    if not filtro == None:
        registros = registro.objects.filter(registro__icontains = str(filtro))
        return render(request, 'registros.html', {'registros':registros})

    registros = registro.objects.reverse()

    return render(request, 'registros.html', {'registros':registros})

# pagina Proyectos ------------------------------------------------------------------------------------------------------------------

def pag_proyecto(request, id):

    proyectos = proyecto.objects.get(id_proyecto = id)
    integrantes = integrantes_proyecto.objects.filter(id_proyecto = id)
    usuarios = datos_usario.objects.all
    pdfs = pdf.objects.filter(id_proyecto = id)

    return render(request, 'proyecto.html', {'proyectos':proyectos,'integrantes':integrantes, 'usuarios':usuarios, 'pdfs':pdfs})

# editar proyecto -----------------------------------------------------------------------------------------------------------------

def editar_proyecto(request, id):

    proyectos = proyecto.objects.get(id_proyecto = id)

    if request.method == 'POST':
        proyecto_form = ProyectoForm(request.POST, instance = proyectos)

        if proyecto_form.is_valid():

            proyecto_form.save()
            generar_registro(request, 'edito el proyecto ' + id, 0)

            return HttpResponseRedirect('/Lab/proyecto/'+id)
    else:
        proyecto_form = ProyectoForm(instance=proyectos)


    return render(request,'crear_proyecto.html',{'proyectos':proyectos, 'acto':'Editar Proyecto'})

# editar usuario-----------------------------------------------------------------------------------------------------------------///

def editar_usuario(request):

    usuario = str(request.user)

    usuarios = User.objects.get(username=str(request.user))
    datos_usuarios = datos_usario.objects.get(usuario = usuario)

    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST, instance = datos_usuarios)
        cuenta_form = UserCreationForm(request.POST, instance = usuarios)

        if usuario_form.is_valid():
            usuario_form.save()

            generar_registro(request, 'edito sus datos', 0)

            return redirect('proyecto:lista_proyectos')

        if cuenta_form.is_valid():

            cuenta_form.save()

            generar_registro(request, 'edito sus datos', 0)

            return redirect('proyecto:lista_proyectos')

    else:
        usuario_form = UsuarioForm(instance=datos_usario)
        cuenta_form = UserCreationForm(instance = datos_usuarios)


    return render(request,'editar_usuario.html',{'datos':datos_usuarios,'id':datos_usuarios.id_usuario,'menu':1})

# borrar integrante ------------------------------------------------------------------------------------------------------------------

def borrar_integrante(request, id, us):

    integrante = integrantes_proyecto.objects.get(id = us)
    usuario_con = datos_usario.objects.get(id_usuario = integrante.id_usuario.id_usuario)
    integrante.delete()

    generar_registro(request, 'borro a ' + usuario_con.nombre + ' ' + usuario_con.primer_ap + ' (' + usuario_con.id_usuario + ')' + ' del proyecto ' + id , 0)

    return HttpResponseRedirect('/Lab/integrantes/'+id)

# Inicio Sesion--------------------------------------------------------------------------------------------------------------

class Sesion(FormView):
    template_name ='inicio_sesion.html'
    form_class = SesionForm
    success_url = reverse_lazy('proyecto:lista_proyectos')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            generar_registro(request, 'inicio sesion', 0)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Sesion,self).dispatch(request, *args, **kwargs)

    def form_valid(self,form):
        login(self.request,form.get_user())
        return super(Sesion,self).form_valid(form)

def salirUsuario(request):
    generar_registro(request, 'Cerror Sesion', 0)
    logout(request)
    return HttpResponseRedirect('/Lab/sesion')
#"""
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



#def consultaID():
    #id =
    #return
