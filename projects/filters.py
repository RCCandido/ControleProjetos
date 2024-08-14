import django_filters

from .models import Usuario

class UsuarioFilter(django_filters.FilterSet):
  name = django_filters.CharFilter(lookup_expr='icontains')
  email = django_filters.CharFilter(lookup_expr='icontains')

  class Meta:
      model = Usuario
      fields = ('name', 'email')