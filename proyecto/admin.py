from django.contrib import admin
from .models import usuario
from .models import datos_usario
from .models import proyecto
from .models import comentario
from .models import pdf
from .models import integrantes_proyecto
from .models import notificacion
from .models import registro

# Register your models here.

admin.site.register(usuario)
admin.site.register(datos_usario)

admin.site.register(proyecto)
admin.site.register(integrantes_proyecto)
admin.site.register(pdf)
admin.site.register(comentario)
admin.site.register(notificacion)
admin.site.register(registro)
