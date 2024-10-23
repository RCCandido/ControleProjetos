import django_filters
from django.db.models import Q

from .models import Usuario, Cliente, Servicos, Grupos, Empresa, Colaborador

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

class ServicosFilter(django_filters.FilterSet):
  filtro = django_filters.CharFilter(method='filterAny')

  class Meta:
      model = Servicos
      fields = ['codigo','descricao']

  def filterAny(self, queryset, filtro, value):
    return Servicos.objects.filter(
          Q(codigo__icontains=value) |
          Q(descricao__icontains=value)
        )

class GruposFilter(django_filters.FilterSet):
  filtro = django_filters.CharFilter(method='filterAny')

  class Meta:
    model = Grupos
    fields = ['descricao','codigo']

  def filterAny(self, queryset, filtro, value):
    return Grupos.objects.filter(
          Q(descricao__icontains=value) |
          Q(codigo__icontains=value)
        )

class EmpresaFilter(django_filters.FilterSet):
  filtro = django_filters.CharFilter(method='filterAny')

  class Meta:
    model = Empresa
    fields = ['codigo','nome','cnpj']

  def filterAny(self, queryset, filtro, value):
    return Empresa.objects.filter(
          Q(nome__icontains=value) |
          Q(cnpj__icontains=value) |
          Q(codigo__icontains=value)
        )

class ColaboradorFilter(django_filters.FilterSet):
  filtro = django_filters.CharFilter(method='filterAny')

  class Meta:
    model = Colaborador
    fields = ['codigo','nome']

  def filterAny(self, queryset, filtro, value):
    return Colaborador.objects.filter(
          Q(nome__icontains=value) |
          Q(codigo__icontains=value)
        )