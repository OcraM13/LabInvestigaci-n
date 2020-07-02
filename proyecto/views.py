#! / usr / bin / python
# - * - codificación: latin-1 - * -
import os, sys
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
from .forms import lan_pageFrom
from .forms import documentosFrom
from .forms import documentosFrom
from .models import proyecto
from .models import integrantes_proyecto
from .models import comentario
from .models import datos_usario
from .models import pdf
from .models import registro
from .models import lan_page
from .models import documentos
from .filters import ProyectosFiltros
from .filters import RegistroFiltros
#from Lab_Investigacion.views import index
import random

from django.utils.encoding import force_bytes

def to_unicode_or_bust(obj, encoding="latin1"):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj=unicode(obj, encoding)
    return obj

# variables intancia

adminA = 'A'
adminD = 'D'

# Create your views here.

def pag404(request):
    return render(request, 'error404.html')

def inicio(request):
    if request.user.is_authenticated:
        return lista_proyectos(request)

    lan = lan_page.objects.filter(visible = '1')

    return render(request, 'inicio.html', {'landing':lan,'activo':'1'})

def ejemplo(request):
    return render(request, 'ejemplo.html')

# crear proyecto ------------------------------------------------------------------------------------------------------------

def crear_proyecto(request):

    if not datos_usario.objects.filter(usuario=str(request.user)):
        return crear_usuario_oficial(request)

    tipo = 0
    usuarios = datos_usario.objects.get(usuario=str(request.user))

    if adminA == usuarios.id_usuario[0]:
        tipo = 1

    if request.method == 'POST':
        proyecto_form = ProyectoForm(request.POST)
        print(proyecto_form)
        if proyecto_form.is_valid():
            num =""

            post = proyecto_form.save(commit=False)

            comprobarcion = True

            while comprobarcion:
                num = generar_numero('P')
                post.id_proyecto = num

                if proyecto.objects.filter(id_proyecto = num):
                    comprobarcion = True
                else:
                    comprobarcion = False

            post.save()

            usuarios = datos_usario.objects.get(usuario=str(request.user))

            if adminA == usuarios.id_usuario[0]:
                tipo = 1

            en = ""

            if usuarios.id_usuario[0] == 'E':
                en = "Integrante"
            else:
                en = "Asesor"

            us = usuarios.id_usuario

            integrantes = integrantes_proyecto(id_proyecto = num, id_usuario = us , encargo = en)

            integrantes.save()

            generar_registro(request, 'creo proyecto ' + num, 0)
            return HttpResponseRedirect('/Lab/integrantes/'+post.id_proyecto)

    else:
        proyecto_form = ProyectoForm()

    return render(request, 'crear_proyecto.html',{'proyectos':'ID','acto':'Crear Proyecto','id':'ID','admin':tipo})

# crear cuenta ---------------------------------------------------------------------------------------------------------------

def crear_cuenta(request):

    usuarios = datos_usario.objects.get(usuario=str(request.user))

    if adminA != usuarios.id_usuario[0]:
        return pag404(request)

    if request.method == 'POST':
        post_usuario = UsuarioForm(request.POST)

        if post_usuario.is_valid():

            num = ""

            post_u = post_usuario.save(commit=False)

            comprobar = True

            while comprobar:

                if post_u.tipo == '1':
                    num = generar_numero('E')

                if post_u.tipo == '2':
                    num = generar_numero('D')

                if post_u.tipo == '3':
                    num = generar_numero('A')

                if datos_usario.objects.filter(id_usuario = num):
                    comprobar = True
                else:
                    comprobar = False

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

                return HttpResponseRedirect('/')
            else:
                messages.info(request, 'Datos Invalidos')
        else:
            messages.info(request, 'Datos Invalidos')
    else:
        usuarios_form = UserCreationForm()
        datos_form = UsuarioForm()

    return render(request,'editar_usuario.html',{'usuario':usuario, 'cero':0, 'tipo':tipo, 'form':usuarios_form})

# subur landing page ------------------------------------------------------------------------------------------------------------------------

def subir_lan(request):

    usuarios = datos_usario.objects.get(usuario=str(request.user))
    if adminA != usuarios.id_usuario[0]:
        return pag404(request)

    land_V = lan_page.objects.filter(visible = '1')
    land_N = lan_page.objects.filter(visible = '0')
    mensaje = ''

    if request.POST:
        landing = lan_pageFrom(request.POST, request.FILES)
        landing.titulo = request.POST.get('titulo')
        landing.imagen = request.FILES.get('imagen')
        landing.descripcion = request.POST.get('descripcion')
        landing.link = request.POST.get('link')
        landing.visible = request.POST.get('visible')

        if landing.is_valid():
            landing.save()
        else:
          mensaje = 'Datos Invalidos'

    else:
        landing = lan_pageFrom()
        print(landing)

    return render(request, 'lan_page.html', {'lan_V':land_V, 'land_N':land_N, 'mensaje':mensaje})

def act_lan(request, id):

    usuarios = datos_usario.objects.get(usuario=str(request.user))
    if adminA != usuarios.id_usuario[0]:
        return pag404(request)

    anuncio = lan_page.objects.get(id = id)
    anuncio.visible = '1'

    anuncio.save()

    return subir_lan(request)

def dec_lan(request, id):

    usuarios = str(request.user)
    if adminA != usuarios.id_usuario[0]:
        return pag404(request)

    anuncio = lan_page.objects.get(id = id)
    anuncio.visible = '0'

    anuncio.save()

    return subir_lan(request)

# subur documento ------------------------------------------------------------------------------------------------------------------------

def subir_documento(request):

    usario = datos_usario

    try:
        usuarios = datos_usario.objects.get(usuario = str(request.user))
    except Exception as e:
        return pag404(request)

    if adminA != usuarios.id_usuario[0]:
        return pag404(request)

    consulta = documentos.objects.all()

    if request.POST:
        doc = documentosFrom(request.POST, request.FILES)
        doc.documento_nombre = request.POST.get('documento_nombre')
        doc.clase = request.POST.get('clase')
        doc.documento = request.POST.get('documento')
        doc.visible = request.POST.get('visible')

        if doc.is_valid():
            doc.save()
        else:
          mensaje = 'Datos Invalidos'

    else:
        doc = documentosFrom()
        #print(doc)

    return render(request, 'documentos.html', {'documento':consulta})

# Activar documento ------------------------------------------------------------------------------------------------------------------------

def act_documento(request, id):

    usario = datos_usario

    try:
        usuarios = datos_usario.objects.get(usuario = request.user)
    except Exception as e:
        return pag404(request)

    if adminA != usuarios.id_usuario[0]:
        return pag404(request)

    doc = documentos.objects.get(id = id)
    doc.visible = '1'
    doc.save()

    return subir_documento(request)

# Des documento ------------------------------------------------------------------------------------------------------------------------

def des_documento(request, id):

    usario = datos_usario

    try:
        usuarios = datos_usario.objects.get(usuario = request.user)
    except Exception as e:
        return pag404(request)

    if adminA != usuarios.id_usuario[0]:
        return pag404(request)

    doc = documentos.objects.get(id = id)
    doc.visible = '0'
    doc.save()

    return subir_documento(request)

# Elimninar documento ------------------------------------------------------------------------------------------------------------------------

def elim_documento(request, id):

    doc = documentos.objects.get(id = id)
    doc.delete()

    return subir_documento(request)

# subur pdf ------------------------------------------------------------------------------------------------------------------------

def nuevo_pdf(request, id):
    tipo = 0
    usuarios = datos_usario.objects.get(usuario=str(request.user))

    if adminA == usuarios.id_usuario[0]:
        tipo = 1

    if request.POST:

        pdf_form = PdfForm(request.POST, request.FILES)

        pdf_form.id_proyecto = request.POST.get('id_proyecto')
        pdf_form.pdf_nombre = request.POST.get('pdf_nombre')
        pdf_form.pdf = request.FILES.get('pdf')

        print(request.FILES.get('pdf'))

        if pdf_form.is_valid():

            pdf_form.save()

            generar_registro(request, 'subio pdf al pryecto' + id, 0)

            return HttpResponseRedirect('/Lab/proyecto/'+id)

    else:
        pdf_form = PdfForm()
        #print(pdf_form)

    return render(request, 'nuevo_pdf.html', {'id':id, 'admin':tipo})

# nuevo miembro --------------------------------------------------------------------------------------------------------------------

def nuevo_miembro(request, id):
    if request.method == 'POST':

        miembro_form = MiembroFrom(request.POST)


        if miembro_form.is_valid():

            post = miembro_form.save(commit=False)

            print(post.id_usuario)
            print(post.encargo)
            print(post.id_proyecto)

            if datos_usario.objects.filter(id_usuario = post.id_usuario):
                post = miembro_form.save()
                generar_registro(request, 'agreo a ' + str(post.id_usuario) +' al proyecto ' + id, 0)
                return HttpResponseRedirect('/Lab/integrantes/'+id)
            else:
                messages.info(request, 'ID de Usuario no Existente')

        else:
            messages.info(request, 'Campos Incorrectos')

    else:
        miembro_form = MiembroFrom()

    us = datos_usario.objects.get(usuario = str(request.user))
    integrantes = integrantes_proyecto.objects.filter(id_proyecto = id)
    usuarios = datos_usario.objects.all

    return render(request, 'nuevo_miembro.html', {'id':id,'us':'Us Id '+us.id_usuario, 'integrantes':integrantes, 'usuarios':usuarios})

# comentarios ------------------------------------------------------------------------------------------------------------------

def comentarios(request,id):

    datos_usuarios = datos_usario.objects.get(usuario=str(request.user))
    tipo = 0

    if adminA == datos_usuarios.id_usuario[0]:
        tipo = 1

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

    return render(request, 'comentarios.html',{'us':id_us,'id':id, 'comentarios':comentarios, 'usuarios':usuarios, 'admin':tipo})

# lista Proyectos ------------------------------------------------------------------------------------------------------------------

def lista_proyectos(request):

    def __str__(self):
        return self.name.encode('utf8')

    if not datos_usario.objects.filter(usuario=str(request.user)):
        return crear_usuario_oficial(request)

    if not datos_usario.objects.filter(usuario=str(request.user)):
        return pag404(request)

    id = datos_usario.objects.get(usuario=str(request.user))

    tipo = 0
    print('pm')

    if adminA == id.id_usuario[0]:
        tipo = 1


    usuario = integrantes_proyecto.objects.filter(id_usuario=id.id_usuario)

    filtro = request.GET.get('filtro')

    if not filtro == None:
        proyectos = proyecto.objects.filter(Q(id_proyecto__icontains = str(filtro))|Q(nombre_proyecto__icontains = str(filtro))).reverse()
        return render(request, 'lista_proyectos.html', {'proyectos':proyectos,'usuario':usuario, 'id':id.id_usuario, 'admin':tipo})

    proyectos = proyecto.objects.all().reverse()

    return render(request, 'lista_proyectos.html', {'proyectos':proyectos,'usuario':usuario, 'id':id.id_usuario, 'admin':tipo})

# lista Sintesis ------------------------------------------------------------------------------------------------------------------

def lista_sintesis(request):

    proyectos = proyecto.objects.all

    return render(request, 'lista_sin.html', {'proyectos':proyectos})

# lista Registros ------------------------------------------------------------------------------------------------------------------

def lista_registros(request):

    usuarios = datos_usario.objects.get(usuario=str(request.user))

    if adminA != usuarios.id_usuario[0]:
        return pag404(request)

    if not User.is_authenticated:
        return lista_proyectos(request)

    filtro = request.GET.get('filtro')

    if not filtro == None:
        registros = registro.objects.filter(registro__icontains = str(filtro)).order_by('-id')
        return render(request, 'registros.html', {'registros':registros})

    registros = registro.objects.all().order_by('-id')

    return render(request, 'registros.html', {'registros':registros})

# pagina Proyectos ------------------------------------------------------------------------------------------------------------------

def pag_proyecto(request, id):

    tipo = 0
    usuarios = datos_usario.objects.get(usuario=str(request.user))

    if adminA == usuarios.id_usuario[0]:
        tipo = 1

    if 'D' == usuarios.id_usuario[0]:
        tipo = 2

    print(tipo)

    proyectos = proyecto.objects.get(id_proyecto = id)
    integrantes = integrantes_proyecto.objects.filter(id_proyecto = id)
    comprobar = integrantes_proyecto.objects.filter(Q(id_proyecto = id)&Q(id_usuario = usuarios.id_usuario))
    if tipo != 1:
        if not integrantes_proyecto.objects.filter(Q(id_proyecto = id)&Q(id_usuario = usuarios.id_usuario)):
            print('hola')
            return pag404(request)

    usuarios = datos_usario.objects.all

    doc = documentos.objects.all

    pdfs = pdf.objects.filter(id_proyecto = id)

    return render(request, 'proyecto.html', {'proyectos':proyectos,'integrantes':integrantes, 'usuarios':usuarios, 'pdfs':pdfs, 'admin':tipo, 'doc':doc})

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

    if not datos_usario.objects.filter(usuario=str(request.user)):
        return HttpResponseRedirect('/Lab/crear_usuario')

    usuarios = User.objects.get(username=str(request.user))
    datos_usuarios = datos_usario.objects.get(usuario = usuarios)
    tipo = 0

    if adminA == datos_usuarios.id_usuario[0]:
        tipo = 1

    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST, instance = datos_usuarios)
        cuenta_form = UserCreationForm(request.POST, instance = usuarios)

        if usuario_form.is_valid():
            usuario_form.save()

            generar_registro(request, 'edito sus datos', 0)

            return lista_proyectos(request)

        if cuenta_form.is_valid():

            cuenta_form.save()

            generar_registro(request, 'edito sus datos', 0)

            return lista_proyectos(request)

    else:
        usuario_form = UsuarioForm(instance=datos_usario)
        cuenta_form = UserCreationForm(instance = datos_usuarios)


    return render(request,'editar_usuario.html',{'datos':datos_usuarios,'id':datos_usuarios.id_usuario,'menu':tipo, 'cero':1, 'admin':tipo})

# borrar integrante ------------------------------------------------------------------------------------------------------------------

def borrar_integrante(request, id, us):

    integrante = integrantes_proyecto.objects.get(id = us)
    usuario_con = datos_usario.objects.get(id_usuario = integrante.id_usuario)
    integrante.delete()

    if integrantes_proyecto.objects.filter(id_proyecto = id):
        generar_registro(request, 'borro a ' + usuario_con.nombre + ' ' + usuario_con.primer_ap + ' (' + usuario_con.id_usuario + ')' + ' del proyecto ' + id , 0)
    else:
        borrar = proyecto.objects.get(id_proyecto = id)
        borrar.delete()
        generar_registro(request, 'Proyecto borrado por '+ usuario_con.nombre + ' ' + usuario_con.primer_ap + 'por falta de integrantes' , 0)
        generar_registro(request, 'borro a ' + usuario_con.nombre + ' ' + usuario_con.primer_ap + ' (' + usuario_con.id_usuario + ')' + ' del proyecto ' + id , 0)
        return pag_proyecto(request, id)

    return HttpResponseRedirect('/Lab/integrantes/'+id)

# borrar Comentario ------------------------------------------------------------------------------------------------------------------

def borrar_comentario(request, doc, id):

    com = comentario.objects.get(id = id)
    com.delete()

    return HttpResponseRedirect('/Lab/comentarios/'+doc)

# borrar pdf ------------------------------------------------------------------------------------------------------------------

def borrar_pdf(request, pro, id):

    doc = pdf.objects.get(id_pdf = id)
    doc.delete()

    return HttpResponseRedirect('/Lab/proyecto/'+pro)

# Inicio Sesion--------------------------------------------------------------------------------------------------------------

class Sesion(FormView):
    template_name ='inicio_sesion.html'
    form_class = SesionForm
    success_url = reverse_lazy('proyecto:lista_proyectos')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Sesion,self).dispatch(request, *args, **kwargs)

    def form_valid(self,form):
        login(self.request,form.get_user())
        #generar_registro(request, 'inicio sesion', 0)
        return super(Sesion,self).form_valid(form)

def salirUsuario(request):
    generar_registro(request, 'Cerror Sesion', 0)
    logout(request)
    return HttpResponseRedirect('/')
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
