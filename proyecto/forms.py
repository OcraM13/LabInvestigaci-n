#! / usr / bin / python
# - * - codificación: latin-1 - * -
import os, sys
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import proyecto
from .models import usuario
from .models import datos_usario
from .models import pdf
from .models import integrantes_proyecto
from .models import comentario
from .models import usuario
from .models import registro
from .models import lan_page
from .models import documentos

"""
class SesionForm(forms.ModelForm):
    class Meta:
        model = usuario
        fields = ['usuario','contraseña']
"""
class SesionForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(SesionForm, self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de Usuario'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'

#"""
class ProyectoForm(forms.ModelForm):
    class Meta:
        model = proyecto
        fields = ['id_proyecto','clase','nombre_proyecto','nombre_sin','sintesis','porsentaje']

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = datos_usario
        fields = ['id_usuario','usuario','nombre','primer_ap','segundo_ap','telefono', 'tipo']

class CuentaForm(forms.ModelForm):
    class Meta:
        model = usuario
        fields = ['usuario','contraseña']

class PdfForm(forms.ModelForm):
    class Meta:
        model = pdf
        fields = ['id_proyecto', 'pdf_nombre', 'pdf']

class MiembroFrom(forms.ModelForm):
    class Meta:
        model = integrantes_proyecto
        fields = ['id_proyecto','id_usuario','encargo']

class ComentarioFrom(forms.ModelForm):
    class Meta:
        model = comentario
        fields =['id_pdf','id_usuario','text_comentario']

class RegistroFrom(forms.ModelForm):
    class Meta:
        model = registro
        fields =['registro']

class lan_pageFrom(forms.ModelForm):
    class Meta:
        model = lan_page
        fields = ['titulo','imagen','descripcion','link','visible']

class documentosFrom(forms.ModelForm):
    class Meta:
        model = documentos
        fields = ['documento','documento_nombre','clase','visible']
