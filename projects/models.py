from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Usuario(AbstractUser):
  
  TIPO = (('1', "Colaborador"), ("2", "Cliente"))
  PERFIS = (
    ('N1', "Nivel 1"), 
    ("N2", "Nivel 2"),
    ("N3", "Nivel 3"),
    ("N4", "Nivel 4"),
    ("N5", "Nivel 5"),
    )


  username = None # desabilita o uso do username
  USERNAME_FIELD = 'user_id'

  user_id = models.IntegerField(primary_key=True)
  name = models.CharField(verbose_name="Nome", max_length=200, null=False, blank=False)
  email = models.EmailField('E-mail', unique=True)
  password = models.CharField(verbose_name="Senha", max_length=30, null=False, blank=False)
  password2 = models.CharField(verbose_name="Confirmação da Senha", max_length=30, null=False, blank=False)
  active = models.BooleanField(default=True, verbose_name="Usuário ativo ?")
  tipo = models.CharField(verbose_name="Tipo", max_length=1, null=False, blank=False, choices=TIPO)
  perfil = models.CharField(verbose_name="Peril", max_length=3, null=False, blank=False, choices=PERFIS)
  resetpsw = models.BooleanField(default=True, verbose_name="Altera Senha ?")
  usefilter = models.BooleanField(default=True, verbose_name="Permite o uso de Filtros ?")

  def set_password(self, raw_password):
    self.password = make_password(raw_password)
    self.password2 = make_password(raw_password)
    self.resetpsw = False
    self.save()
    return 
 
  class Meta:
    verbose_name_plural = "Usuários"
    ordering = ('name',)

  def __str__(self):
    return self.name
  
class Niveis(models.Model):
  SN = (
    ('S', 'Sim'),
    ('N', 'Não'),
  )
  STATUS = (('B', "Bloqueado"), ("L", "Liberado"))

  nivel_id = models.AutoField(primary_key=True)
  descricao = models.CharField(verbose_name="Descrição", max_length=200, null=False, blank=False)
  rotina = models.CharField(verbose_name="Rotina", max_length=80)
  inclusao = models.CharField(verbose_name="Incluir", max_length=1, null=False, blank=False, choices=SN)
  edicao = models.CharField(verbose_name="Editar", max_length=1, null=False, blank=False, choices=SN)
  exclusao = models.CharField(verbose_name="Excluir", max_length=1, null=False, blank=False, choices=SN)
  logs = models.CharField(verbose_name="Logs", max_length=1, null=False, blank=False, choices=SN)
  filtro = models.CharField(verbose_name="Filtro", max_length=1, null=False, blank=False, choices=SN)
  active = models.BooleanField(default=True, verbose_name="Nível ativo ?")


class Empresa(models.Model):
  codigo = models.CharField(verbose_name="Código", unique=True, max_length=6, null=False, blank=False)
  nome = models.CharField(verbose_name="Empresa", max_length=200, null=False, blank=False)
  
  def __str__(self):
    return self.nome
  
  class Meta:
    verbose_name_plural = "Empresas"

class Servicos(models.Model):
  TIPOS = (
    ('pontual', 'Pontual'),
    ('sustentacao', 'Sustentação'),
    ('sd', 'Service Desk'),
    ('projeto', 'Projeto'),
    ('hradicional', 'Hora Adicional'),
  )

  codigo = models.CharField(verbose_name="Código", max_length=6, null=False, blank=False)
  descricao = models.CharField(verbose_name="Descrição", max_length=80, null=False, blank=False)
  versao = models.CharField(verbose_name="Versão", max_length=3, null=False, blank=False)
  cliente = models.CharField(verbose_name="Cliente", max_length=6, null=False, blank=False)
  nomeCliente = models.CharField(verbose_name="Nome", max_length=80, null=False, blank=False)
  tipo = models.CharField(verbose_name="Tipo", max_length=20,  choices=TIPOS)
  observacao = models.TextField(verbose_name="Observações")

  class Meta:
    verbose_name_plural = "Serviços"