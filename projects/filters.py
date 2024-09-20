import django_filters
from django.db.models import Q

from .models import Usuario

class UsuarioFilter(django_filters.FilterSet):
  #name = django_filters.CharFilter(lookup_expr='icontains', label="Name", )
  name = django_filters.CharFilter(method='filterAny')

  def filterAny(self, queryset, name, value):
    return Usuario.objects.filter(Q(name__in=value) | Q(email__in=(value)))

  class Meta:
      model = Usuario
      fields = '__all__'