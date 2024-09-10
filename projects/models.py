from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils.translation import gettext as _

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

  created_at = models.DateTimeField(auto_now=True)
  updated_at = models.DateTimeField(auto_now=True)
  active = models.BooleanField(default=True, verbose_name="Nível ativo ?")

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
    ordering = ('user_id',)

  def __str__(self):
    return self.name

  username = None # desabilita o uso do username
  USERNAME_FIELD = 'user_id'
  
  created_at = models.DateTimeField(auto_now=True)
  updated_at = models.DateTimeField(auto_now=True)
  active = models.BooleanField(default=True, verbose_name="Usuário ativo ?")

  user_id = models.AutoField(primary_key=True)
  firstname = models.CharField(verbose_name="Primeiro Nome", max_length=20, null=False, blank=False)
  name = models.CharField(verbose_name="Nome Completo", max_length=200, null=False, blank=False)
  email = models.EmailField('E-mail', unique=True, null=False, blank=False)
  password = models.CharField(verbose_name="Senha", max_length=30, null=False, blank=False)
  password2 = models.CharField(verbose_name="Confirmação da Senha", max_length=30, null=False, blank=False)
  tipo = models.CharField(verbose_name="Tipo", max_length=1, null=False, blank=False, choices=getTipos())
  perfil = models.ForeignKey(
    Niveis,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
  )
  resetpsw = models.BooleanField(default=True, verbose_name="Altera Senha ?")
  usefilter = models.BooleanField(default=True, verbose_name="Permite o uso de Filtros ?")
  
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
  updated_at = models.DateTimeField(auto_now=True)
  active = models.BooleanField(default=True, verbose_name="Empresa ativa ?")
  codigo = models.AutoField(primary_key=True)

  nome = models.CharField(
      verbose_name="Empresa", max_length=200, null=False, blank=False
  )

  cnpj = models.CharField(verbose_name="CNPJ", max_length=18, default="")
  endereco = models.CharField(verbose_name="Endereço", blank=True, max_length=250, default="")
  cidade = models.CharField(verbose_name="Cidade", max_length=80, default="")
  estado = models.CharField(verbose_name="Estado", max_length=2, choices=getUF())
  telefone = models.CharField(verbose_name="Telefone", max_length=20, default="")
  dados_bancarios = models.TextField(verbose_name="Informações Bancarias", null=True, blank=True, default="")
  imposto = models.FloatField(_("imposto"))

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
  
  created_at = models.DateTimeField(auto_now=True)
  updated_at = models.DateTimeField(auto_now=True)
  active = models.BooleanField(default=True, verbose_name="Cliente ativo ?")
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
  
  class Meta:
    verbose_name_plural = "Clientes"

  def __str__(self):
      return self.nome

class Servicos(models.Model):
  
  def getTipos():
    TIPOS = (
      ('Pontual', 'Pontual'),
      ('Sustentação', 'Sustentação'),
      ('Service Desk', 'Service Desk'),
      ('Projeto', 'Projeto'),
      ('Hora Adicional', 'Hora Adicional'),
    )
    return TIPOS
  
  def getEtapasComercial():
    TIPOS = (
      ('Oportunidade', 'Oportunidade'),
      ('Proposta', 'Proposta'),
      ('Fechado', 'Fechado'),
      ('Perdido', 'Perdido'),
    )
    return TIPOS
  
  def getEtapasTecnicas():
    TIPOS = (
      ('DOS16', 'DOS16'),
      ('Definição de Analista', 'Definição de Analista'),
      ('Repasse', 'Repasse'),
      ('Desenvolvimento', 'Desenvolvimento'),
      ('Validação', 'Validação'),
      ('Revisão', 'Revisão'),
      ('Acompanhamento', 'Acompanhamento'),
      ('Finalizado', 'Finalizado'),
      ('Outros', 'Outros'),
    )
    return TIPOS
  
  def getNextCodigo():
    codigo = 'ERP-%04d' % (Servicos.objects.count()+1)
    return codigo

  created_at = models.DateTimeField(auto_now=True)
  updated_at = models.DateTimeField(auto_now=True)
  codigo = models.CharField(primary_key=True, max_length=8)

  descricao = models.CharField(verbose_name="Descrição", max_length=80, null=False, blank=False)
  versao = models.CharField(verbose_name="Versão", max_length=3, null=False, blank=False)
  
  cliente = models.ForeignKey(
    Cliente,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
  )

  tipo = models.CharField(verbose_name="Tipo", max_length=20,  choices=getTipos())
  valor_hora = models.DecimalField(verbose_name="Valor Hora", max_digits=6, decimal_places=2)
  comissao = models.DecimalField(verbose_name="% Comissão", max_digits=6, decimal_places=2)
  valor_comissao = models.DecimalField(verbose_name="R$ Valor Comissao", max_digits=6,decimal_places=2,null=True, blank=True)
  imposto = models.DecimalField(verbose_name="% Imposto", max_digits=6, decimal_places=2,null=True, blank=True)
  valor_imposto = models.DecimalField(verbose_name="R$ Imposto", max_digits=6, decimal_places=2,null=True, blank=True)
  horas_especificacao = models.DecimalField(verbose_name="Horas Especificação", max_digits=6, decimal_places=2,null=True, blank=True)
  horas_tecnicas = models.DecimalField(verbose_name="Horas Técnicas", max_digits=6, decimal_places=2,null=True, blank=True)
  desconto = models.DecimalField(verbose_name="% Desconto", max_digits=6, decimal_places=2,null=True, blank=True)
  valor_desconto = models.DecimalField(verbose_name="R$ Desconto", max_digits=6,decimal_places=2,null=True, blank=True)
  valor_recebido = models.DecimalField(verbose_name="R$ Valor Recebido", max_digits=8,decimal_places=2,null=True, blank=True)
  base_comissao = models.DecimalField(verbose_name="Base Comissao", max_digits=6,decimal_places=2,null=True, blank=True)
  custo_operacional = models.DecimalField(verbose_name="Custo Operacional", max_digits=6, decimal_places=2,null=True, blank=True)
  liquido = models.DecimalField(verbose_name="R$ Liquido", max_digits=8, decimal_places=2,null=True, blank=True)
  valor_bruto = models.DecimalField(verbose_name="R$ Valor Bruto", max_digits=8, decimal_places=2,null=True, blank=True)
  horas_save = models.DecimalField(verbose_name="Horas Save", max_digits=6, decimal_places=2,null=True, blank=True)
  horas_execucao = models.DecimalField(verbose_name="Horas Execução", max_digits=6, decimal_places=2,null=True, blank=True)
  etapa_comercial = models.CharField(verbose_name="Etapa Comercial", max_length=30,  choices=getEtapasComercial())
  etapa_tecnica = models.CharField(verbose_name="Etapa Técnica", max_length=30,  choices=getEtapasTecnicas())
  justificativa = models.TextField(verbose_name="Justificativa")
  anotacoes = models.TextField(verbose_name="Anotações")
  versao_valida = models.CharField(verbose_name="Versão Valida", max_length=3)
  parcelamento = models.CharField(verbose_name="Parcelamento", max_length=50, blank=True, null=True)
  
  #def save(self, *args, **kwargs):
  #  self.valor_hora = float(self.valor_hora)
  #  super(Servicos, self).save(*args, **kwargs)

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

  created_at = models.DateTimeField(auto_now=True)
  updated_at = models.DateTimeField(auto_now=True)
  active = models.BooleanField(default=True, verbose_name="Projeto ativo ?")
  codigo = models.CharField(primary_key=True, max_length=8)

  name = models.CharField(
      verbose_name="Descrição", null=False, blank=False, max_length=200
  )
  
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

class Colaborador(models.Model):

  def getFuncao():
    TIPOS = (
      ("1", "Arquiteto"), 
      ("2", "Analista"),
      ("3", "Desenvolvedor"),
      ("4", "Gerente de Projetos"),
      ("5", "QA"),
      ("6", "Gerente Geral"),
      ("7", "Diretor"),
    )
    return TIPOS

  created_at = models.DateTimeField(auto_now=True)
  updated_at = models.DateTimeField(auto_now=True)
  active = models.BooleanField(default=True, verbose_name="Colaborador ativo ?")
  codigo = models.AutoField(primary_key=True)
   
  nome = models.CharField(
    verbose_name="Nome", null=False, blank=False, max_length=200
  )

  cpf = models.CharField(
    verbose_name="CPF", null=False, blank=False, max_length=14
  )

  endereco = models.CharField(verbose_name="Endereço", blank=True, max_length=250, default="")
  cidade = models.CharField(verbose_name="Cidade", max_length=80, default="")
  bairro = models.CharField(verbose_name="Bairro", max_length=50, blank=True)
  estado = models.CharField(verbose_name="Estado", max_length=2, choices=Empresa.getUF())
  telefone = models.CharField(verbose_name="Telefone", max_length=20, default="")
  email = models.EmailField(verbose_name='E-mail')
  dados_bancarios = models.TextField(verbose_name="Informações Bancarias", null=True, blank=True, default="")
  valor_hora = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, default=0)
  valor_fixo = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
  comissao = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
  funcao = models.CharField(verbose_name="Função", max_length=20, choices=getFuncao())
  periodo_lancamento = models.DateField(
      verbose_name="Periodo Lancto", 
      auto_now=False,
      auto_now_add=False,
      null=True, 
      blank=True,
  )
  
  class Meta:
      verbose_name_plural = "Colaboradores"

  def __str__(self):
      return self.nome

class Valores(models.Model):
 
  def getTipos():
    TIPOS = (
      ('Empresa', 'Empresa'),
      ('Colaborador', 'Colaborador'),
      ('Cliente', 'Cliente'),
      ('Servico', 'Servico'),
    )
    return TIPOS

  created_at = models.DateTimeField(auto_now=True)
  updated_at = models.DateTimeField(auto_now=True)
  active = models.BooleanField(default=True, verbose_name="Registro ativo ?")
  valor_id = models.AutoField(primary_key=True)
  
  tipo = models.CharField(verbose_name="Tipo", max_length=20, choices=getTipos())
  codigo = models.CharField(verbose_name="Codigo", max_length=6, null=False, blank=False)

  data = models.DateField(
    verbose_name="Data", 
    auto_now=True,
    auto_now_add=False,
    null=False, 
    blank=False,
  )

  valor_hora = models.DecimalField(verbose_name="Valor Hora", max_digits=6, decimal_places=2, null=True, blank=True)
  valor_fixo = models.DecimalField(verbose_name="Valor Fixo", max_digits=6, decimal_places=2, null=True, blank=True)
  comissao = models.DecimalField(verbose_name="% Comissão", max_digits=6, decimal_places=2, null=True, blank=True)
  imposto = models.DecimalField(verbose_name="% Imposto", max_digits=6, decimal_places=2, null=True, blank=True)
  desconto = models.DecimalField(verbose_name="% Desconto", max_digits=6, decimal_places=2, null=True, blank=True)
  observacao = models.TextField(verbose_name="Observações")
  
  class Meta:
      verbose_name_plural = "Valores"

  def __str__(self):
      return self.codigo
  