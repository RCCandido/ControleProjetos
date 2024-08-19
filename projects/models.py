from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Niveis(models.Model):
    SN = (
        ('S', 'Sim'),
        ('N', 'Não'),
    )
    STATUS = (("B", "Bloqueado"), ("L", "Liberado"))

    ROTINAS = (
        ("0", "Todas"),
        ("1", "Empresas"),
        ("2", "Projetos"),
        ("3", "Niveis"),
        ("4", "Usuários"),
        ("5", "Serviços"),
        ("6", "Relatórios"),
    )
    nivel_id = models.AutoField(primary_key=True)
    descricao = models.CharField(
      verbose_name="Descrição", max_length=200, null=False, blank=False
    )
    rotina = models.CharField(verbose_name="Rotina", max_length=80, choices=ROTINAS)

    inclusao = models.CharField(
      verbose_name="Incluir", max_length=1, null=False, blank=False, choices=SN
    )
    edicao = models.CharField(
      verbose_name="Editar", max_length=1, null=False, blank=False, choices=SN
    )
    exclusao = models.CharField(
      verbose_name="Excluir", max_length=1, null=False, blank=False, choices=SN
    )
    logs = models.CharField(
      verbose_name="Logs", max_length=1, null=False, blank=False, choices=SN
    )
    filtro = models.CharField(
      verbose_name="Filtro", max_length=1, null=False, blank=False, choices=SN
    )
    active = models.BooleanField(default=True, verbose_name="Nível ativo ?")
    created_at = models.DateTimeField(auto_now=True)

    def get_niveis():
        return Niveis.objects.all()['descricao']

    def __str__(self):
        return self.descricao

    def __unicode__(self):
        return self.descricao

class Usuario(AbstractUser):

    TIPO = (("1", "Colaborador"), ("2", "Cliente"))

    username = None # desabilita o uso do username
    USERNAME_FIELD = 'user_id'

    user_id = models.IntegerField(primary_key=True)
    firstname = models.CharField(verbose_name="Primeiro Nome", max_length=20, null=False, blank=False)
    name = models.CharField(verbose_name="Nome Completo", max_length=200, null=False, blank=False)
    email = models.EmailField('E-mail', unique=True)
    password = models.CharField(verbose_name="Senha", max_length=30, null=False, blank=False)
    password2 = models.CharField(verbose_name="Confirmação da Senha", max_length=30, null=False, blank=False)
    active = models.BooleanField(default=True, verbose_name="Usuário ativo ?")
    tipo = models.CharField(verbose_name="Tipo", max_length=1, null=False, blank=False, choices=TIPO)
    perfil = models.ForeignKey(
        Niveis,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    resetpsw = models.BooleanField(default=True, verbose_name="Altera Senha ?")
    usefilter = models.BooleanField(default=True, verbose_name="Permite o uso de Filtros ?")
    created_at = models.DateTimeField(auto_now=True)

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

class Empresa(models.Model):
  codigo = models.CharField(
      verbose_name="Código", unique=True, max_length=6, null=False, blank=False
  )
  nome = models.CharField(
      verbose_name="Empresa", max_length=200, null=False, blank=False
  )
  created_at = models.DateTimeField(auto_now=True)


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
  created_at = models.DateTimeField(auto_now=True)

  class Meta:
    verbose_name_plural = "Serviços"

class Log(models.Model):
  log_id = models.AutoField(primary_key=True)
  processo = models.CharField(verbose_name="Rotina", max_length=80)
  usuario = models.CharField(
      verbose_name="Nome", max_length=200, null=False, blank=False
  )
  email = models.EmailField("E-mail", unique=True)
  log_at = models.DateTimeField(auto_now=True)

  class Meta:
      verbose_name_plural = "Logs"

class Projetos(models.Model):

  STATUS = (
    ('0', 'Orçamento'),
    ('1', 'Aprovado'),
    ('2', 'Iniciado'),
    ('3', 'Em Desenvolvimento'),
    ('4', 'Em Teste'),
    ('5', 'Em Homologação'),
    ('6', 'Homologado'),
    ('7', 'Em Produção'),
    ('8', 'Finalizado'),
  )

  codigo = models.CharField(primary_key=True, verbose_name="Código", max_length=8, blank=False, unique=True)
  name = models.CharField(verbose_name="Descrição", null=False, blank=False, max_length=200)
  created_at = models.DateTimeField(auto_now=True)
  updated_at = models.DateTimeField(auto_now=True)
  cliente = models.CharField(verbose_name="Cliente", max_length=50)
  responsavel = models.CharField(verbose_name="Responsável", max_length=50)
  arquiteto = models.CharField(verbose_name="Arquiteto", max_length=50)
  data_inicio = models.DateField(verbose_name="Inicio", auto_now=False, auto_now_add=False)
  data_entrega = models.DateField(verbose_name="Entrega", auto_now=False, auto_now_add=False)
  desenvolvedor = models.CharField(verbose_name="Desenvolvedor", max_length=50)
  status = models.CharField(verbose_name="Status", max_length=1, choices=STATUS)

  class Meta:
    verbose_name_plural = "Projetos"
