import django_filters
from django.db.models import Q

from .models import Usuario, Cliente

class UsuarioFilter(django_filters.FilterSet):
  name = django_filters.CharFilter(method='filterAny')

  class Meta:
      model = Usuario
      fields = ['name']

  def filterAny(self, queryset, name, value):
    return Usuario.objects.filter(
          Q(name__icontains=value) |
          Q(email__icontains=value) |
          Q(tipo__icontains=value) |
          Q(user_id__icontains=value)
        )

class ClienteFilter(django_filters.FilterSet):
  nome = django_filters.CharFilter(method='filterAny')

  class Meta:
      model = Cliente
      fields = ['nome']

  def filterAny(self, queryset, name, value):
    return Cliente.objects.filter(
          Q(nome__icontains=value) |
          Q(cnpj__icontains=value)
        )