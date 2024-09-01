from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Niveis(models.Model):
  
  def getSimNao():
    SN = (
        ('S', 'Sim'),
        ('N', 'Não'),
    )
    return SN

  def getRotinas():
    ROTINAS = (
        ("0", "Todas"),
        ("1", "Empresas"),
        ("2", "Projetos"),
        ("3", "Niveis"),
        ("4", "Usuários"),
        ("5", "Serviços"),
        ("6", "Relatórios"),
    )
    return ROTINAS
  
  def __str__(self):
      return self.descricao

  def __unicode__(self):
      return self.descricao

  nivel_id = models.AutoField(primary_key=True)
  descricao = models.CharField(
    verbose_name="Descrição", max_length=200, null=False, blank=False
  )
  rotina = models.CharField(verbose_name="Rotina", max_length=80, choices=getRotinas())

  inclusao = models.CharField(
    verbose_name="Incluir", max_length=1, null=False, blank=False, choices=getSimNao()
  )
  edicao = models.CharField(
    verbose_name="Editar", max_length=1, null=False, blank=False, choices=getSimNao()
  )
  exclusao = models.CharField(
    verbose_name="Excluir", max_length=1, null=False, blank=False, choices=getSimNao()
  )
  logs = models.CharField(
    verbose_name="Logs", max_length=1, null=False, blank=False, choices=getSimNao()
  )
  filtro = models.CharField(
    verbose_name="Filtro", max_length=1, null=False, blank=False, choices=getSimNao()
  )
  active = models.BooleanField(default=True, verbose_name="Nível ativo ?")
  created_at = models.DateTimeField(auto_now=True)

  class Meta:
    verbose_name_plural = "Niveis"
    ordering = ('nivel_id','descricao',)

  def __str__(self):
    return self.descricao

class Usuario(AbstractUser):

  def getTipos():
    TIPOS = (
      ("1", "Cliente"), 
      ("2", "Colaborador"),
    )
    return TIPOS

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

  username = None # desabilita o uso do username
  USERNAME_FIELD = 'user_id'

  user_id = models.AutoField(primary_key=True)
  firstname = models.CharField(verbose_name="Primeiro Nome", max_length=20, null=False, blank=False)
  name = models.CharField(verbose_name="Nome Completo", max_length=200, null=False, blank=False)
  email = models.EmailField('E-mail', unique=True)
  password = models.CharField(verbose_name="Senha", max_length=30, null=False, blank=False)
  password2 = models.CharField(verbose_name="Confirmação da Senha", max_length=30, null=False, blank=False)
  active = models.BooleanField(default=True, verbose_name="Usuário ativo ?")
  tipo = models.CharField(verbose_name="Tipo", max_length=1, null=False, blank=False, choices=getTipos())
  perfil = models.ForeignKey(
    Niveis,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
  )
  resetpsw = models.BooleanField(default=True, verbose_name="Altera Senha ?")
  usefilter = models.BooleanField(default=True, verbose_name="Permite o uso de Filtros ?")
  created_at = models.DateTimeField(auto_now=True)
  
class Empresa(models.Model):

  def getUF():
    UF = (
      ("AC", "AC"),
      ("AL", "AL"),
      ("AP", "AP"),
      ("AM", "AM"),
      ("BA", "BA"),
      ("CE", "CE"),
      ("DF", "DF"),
      ("ES", "ES"),
      ("GO", "GO"),
      ("MA", "MA"),
      ("MT", "MT"),
      ("MS", "MS"),
      ("MG", "MG"),
      ("PA", "PA"),
      ("PB", "PB"),
      ("PR", "PR"),
      ("PE", "PE"),
      ("PI", "PI"),
      ("RJ", "RJ"),
      ("RN", "RN"),
      ("RS", "RS"),
      ("RO", "RO"),
      ("RR", "RR"),
      ("SC", "SC"),
      ("SP", "SP"),
      ("SE", "SE"),
      ("TO", "TO"),
    )
    return UF

  created_at = models.DateTimeField(auto_now=True)
  codigo = models.CharField(
      primary_key=True,
      verbose_name="Código", unique=True, max_length=6, null=False, blank=False
  )
  nome = models.CharField(
      verbose_name="Empresa", max_length=200, null=False, blank=False
  )

  cnpj = models.CharField(verbose_name="CNPJ", max_length=14, default="")
  endereco = models.CharField(verbose_name="Endereço", blank=True, max_length=250, default="")
  cidade = models.CharField(verbose_name="Cidade", max_length=80, default="")
  estado = models.CharField(verbose_name="Estado", max_length=2, choices=getUF())
  telefone = models.CharField(verbose_name="Telefone", max_length=20, default="")
  dados_bancarios = models.TextField(verbose_name="Informações Bancarias", null=True, blank=True, default="")
  imposto = models.IntegerField(verbose_name="% Imposto", default=0)

  def __str__(self):
    return self.nome

  class Meta:
    verbose_name_plural = "Empresas"
    ordering = ('codigo',)

class Cliente(models.Model):

  def getTipo():
    TIPO = (
      ('F', 'Pessoa Fisica'),
      ('J', 'Pessoa Juridica'),
    )
    return TIPO
  
  codigo = models.AutoField(primary_key=True)
  nome = models.CharField(verbose_name="Nome", null=False, blank=False, max_length=200)
  cnpj = models.CharField(verbose_name="CNPJ", max_length=14)
  ie = models.CharField(verbose_name="IE", max_length=14, blank=True)
  endereco = models.CharField(verbose_name="Endereco", max_length=150, blank=True)
  complemento = models.CharField(verbose_name="Complemento", max_length=50, blank=True)
  bairro = models.CharField(verbose_name="Bairro", max_length=50, blank=True)
  cidade = models.CharField(verbose_name="Cidade", max_length=50, blank=True)
  estado = models.CharField(verbose_name="Estado", max_length=2, choices=Empresa.getUF(), default="")
  email = models.CharField(verbose_name="E-mail", max_length=100, blank=False, default="")
  email_cat = models.CharField(verbose_name="E-mail Cat", max_length=100, default="")
  usa_email_cat = models.CharField(verbose_name="Recebe E-mail Cat?", max_length=1, choices=Niveis.getSimNao(), default="")
  telefone = models.CharField(verbose_name="Telefone", max_length=20, blank=False,default="")
  contatos = models.TextField(verbose_name="Contatos", null=True, blank=True, default="")
  dados_bancarios = models.TextField(verbose_name="Informações Bancárias", null=True, blank=True, default="")
  observacoes = models.TextField(verbose_name="Observações", null=True, blank=True, default="")
  valor_hora_atual = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, default=0)
  perc_desconto_atual = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, default=0)
  active = models.BooleanField(default=True, verbose_name="Cliente ativo ?")

  created_at = models.DateTimeField(auto_now=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    verbose_name_plural = "Clientes"

  def __str__(self):
      return self.nome

class Servicos(models.Model):
  
  def getTipos():
    TIPOS = (
      ('pontual', 'Pontual'),
      ('sustentacao', 'Sustentação'),
      ('sd', 'Service Desk'),
      ('projeto', 'Projeto'),
      ('hradicional', 'Hora Adicional'),
    )
    return TIPOS
    
  codigo = models.CharField(verbose_name="Código", max_length=6, null=False, blank=False)
  descricao = models.CharField(verbose_name="Descrição", max_length=80, null=False, blank=False)
  versao = models.CharField(verbose_name="Versão", max_length=3, null=False, blank=False)
  
  cliente = models.ForeignKey(
    Cliente,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
  )

  tipo = models.CharField(verbose_name="Tipo", max_length=20,  choices=getTipos())
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

  def getStatus():
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
    return STATUS

  codigo = models.CharField(
      primary_key=True, verbose_name="Código", max_length=8, blank=False, unique=True
  )
  name = models.CharField(
      verbose_name="Descrição", null=False, blank=False, max_length=200
  )
  created_at = models.DateTimeField(auto_now=True)
  updated_at = models.DateTimeField(auto_now=True)

  cliente = models.ForeignKey(
    Cliente,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
  )

  responsavel = models.CharField(verbose_name="Responsável", max_length=50)
  arquiteto = models.CharField(verbose_name="Arquiteto", max_length=50)
  data_inicio = models.DateField(
      verbose_name="Inicio", 
      auto_now=False,
      auto_now_add=False,
      null=True, 
      blank=True,
  )
  data_entrega = models.DateField(
      verbose_name="Entrega", 
      auto_now=False, 
      auto_now_add=False,
      null=True, 
      blank=True,
  )
  desenvolvedor = models.CharField(verbose_name="Desenvolvedor", max_length=50)
  status = models.CharField(verbose_name="Status", max_length=1, choices=getStatus())
  qtd_horas_apontadas = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
  qtd_horas_projeto = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
  valor_hora = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
  valor_total = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

  class Meta:
      verbose_name_plural = "Projetos"

  def __str__(self):
      return self.name


  
  