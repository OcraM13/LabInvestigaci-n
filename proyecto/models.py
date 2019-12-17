from django.db import models

# Create your models here.

class usuario(models.Model):
    usuario = models.CharField(max_length = 20, primary_key = True)
    contraseña = models.CharField(max_length = 30, blank = False, null = False)

class datos_usario(models.Model):
    id_usuario = models.CharField(max_length = 5, primary_key = True)
    usuario = models.CharField(max_length = 20)
    nombre = models.CharField(max_length = 20)
    primer_ap = models.CharField(max_length = 20)
    segundo_ap = models.CharField(max_length = 20)
    telefono = models.CharField(max_length = 10)
    tipo = models.CharField(max_length = 4)

class proyecto(models.Model):
    id_proyecto = models.CharField(max_length = 5, primary_key = True)
    clase = models.CharField(max_length = 15)
    nombre_proyecto = models.CharField(max_length = 50)
    nombre_sin = models.CharField(max_length = 30)
    sintesis = models.TextField()
    porsentaje = models.IntegerField()

class integrantes_proyecto(models.Model):
    id = models.AutoField(primary_key = True)
    id_proyecto = models.CharField(max_length = 5)
    id_usuario = models.CharField(max_length = 5)
    encargo = models.CharField(max_length = 10)

class pdf(models.Model):
    id_pdf = models.AutoField(primary_key = True)
    pdf_nombre = models.CharField(max_length = 50, null = True)
    id_proyecto = models.ForeignKey(proyecto, on_delete = models.CASCADE)
    pdf = models.FileField(upload_to='archivos/%Y/%m/%d/', default='')
    #fecha = models.DateTimeField(auto_now = True, auto_now_add = False)

class comentario(models.Model):
    id = models.AutoField(primary_key = True)
    id_pdf = models.ForeignKey(pdf, on_delete = models.CASCADE)
    id_usuario = models.ForeignKey(datos_usario, on_delete = models.CASCADE, default='')
    text_comentario = models.TextField()
    #fecha = models.DateTimeField(auto_now = True)

class notificacion(models.Model):
    id = models.AutoField(primary_key = True)
    id_usuario = models.ForeignKey(datos_usario, on_delete = models.CASCADE, default='')
    id_proyecto = models.ForeignKey(proyecto, on_delete = models.CASCADE)
    notificacion = models.CharField(max_length = 150)

class registro(models.Model):
    id = models.AutoField(primary_key = True)
    registro = models.CharField(max_length = 150)
