import django_filters
from .models import proyecto
from .models import registro


class ProyectosFiltros(django_filters.FilterSet):

    class Meta:
        model: proyecto
        fields = ('id_proyecto', 'clase', 'nombre_proyecto', 'nombre_sin', 'sintesis', 'porsentaje')

class RegistroFiltros(django_filters.FilterSet):

    class Meta:
        model: registro
        fields = ('registro')
