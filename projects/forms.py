from django import forms
from crispy_forms.helper import FormHelper 
from crispy_forms.layout import Layout, Submit, Row, Field 
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML, Div

from .models import Usuario, Empresa, Servicos, Niveis, Projetos, Cliente

class RedefinirSenhaForm(forms.ModelForm):
  email = forms.CharField(disabled=True, required=False)
  password = forms.CharField(
      widget=forms.PasswordInput(), required=True, label="Nova Senha"
  )
  password2 = forms.CharField(
      widget=forms.PasswordInput(), required=True, label="Confirmação da Nova Senha"
  )

  class Meta:
      model = Usuario
      fields = (
          "email",
          "password",
          "password2",
      )

class UsuarioForm(forms.ModelForm):

  email = forms.EmailField(disabled=True, required=False,)

  password = forms.CharField(
    widget=forms.PasswordInput(), disabled=False, required=False
  )

  password2 = forms.CharField(
    widget=forms.PasswordInput(), disabled=False, required=False
  )

  tipo = forms.ChoiceField(
    choices=Usuario.getTipos(),
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )
  
  perfil = forms.ModelChoiceField(
    queryset=Niveis.objects.all().order_by("descricao"),
    to_field_name='nivel_id',
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )

  class Meta:
    model = Usuario
    fields = (
        "firstname",
        "name",
        "email",
        "password",
        "password2",
        "active",
        "tipo",
        "perfil",
        "usefilter",
        "resetpsw",
    )

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_class = ''
    self.helper.layout = Layout(
      Row(
        Column('firstname', css_class='form-control-sm col-sm-4'),
        Column('name', css_class='form-control-sm col-sm-8'),
        css_class='form-row d-flex',
      ),
      Row(
        Column('email', css_class='form-control-sm col-sm-6'),
        Column('tipo', css_class='form-control-sm col-sm-2'),
        Column('perfil', css_class='form-control-sm col-sm-4'),
        css_class='form-row d-flex',
      ),
      Row(
        Column('password',css_class='form-control-sm col-sm-4'),
        Column('password2',css_class='form-control-sm col-sm-4'),
        css_class='form-row d-flex',
      ),
      Row(
        Column('resetpsw', css_class='form-control-sm'),
        Column('active', css_class='form-control-sm'),
        Column('usefilter', css_class='form-control-sm'),
        css_class='form-row d-flex',
      ),
      Div(
        Row(
          Submit('submit', 'Confirmar', css_class='mx-2'),
          HTML('<a class="btn btn-danger" href="{% url "usuarios" %}">Cancelar</a>'),
          css_class='form-row d-flex',
        )
      )
    )

class NewUsuarioForm(UsuarioForm):
  
  email = forms.EmailField(disabled=False, required=True,)

  password = forms.CharField(
      widget=forms.PasswordInput(), required=True, label="Senha"
  )
  
  password2 = forms.CharField(
      widget=forms.PasswordInput(), required=True, label="Repita a Senha"
  )
 
class NivelForm(forms.ModelForm):

  rotina = forms.ChoiceField(
    choices=Niveis.getRotinas(),
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )
  
  inclusao = forms.ChoiceField(
    choices=Niveis.getSimNao(),
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )
  
  edicao = forms.ChoiceField(
    choices=Niveis.getSimNao(),
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )
  
  exclusao = forms.ChoiceField(
    choices=Niveis.getSimNao(),
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )
  
  logs = forms.ChoiceField(
    choices=Niveis.getSimNao(),
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )
  
  filtro = forms.ChoiceField(
    choices=Niveis.getSimNao(),
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )

  class Meta:
      model = Niveis
      fields = "__all__"

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_class = ''
    self.helper.layout = Layout(
      Row(
        Column('descricao', css_class='form-control-sm col-sm-4'),
        Column('rotina', css_class='form-control-sm col-sm-2'),
        css_class='form-row d-flex',
      ),
      Row(
        Column('inclusao', css_class='form-control-sm col-sm-2'),
        Column('edicao', css_class='form-control-sm col-sm-2'),
        Column('exclusao', css_class='form-control-sm col-sm-2'),
        css_class='form-row d-flex',
      ),
      Row(
        Column('logs',css_class='form-control-sm col-sm-4'),
        Column('filtro',css_class='form-control-sm col-sm-4'),
        css_class='form-row d-flex',
      ),
      Row(
        Column('active', css_class='form-control-sm'),
        css_class='form-row d-flex',
      ),
      Div(
        Row(
          Submit('submit', 'Confirmar', css_class='mx-2'),
          HTML('<a class="btn btn-danger" href="{% url "niveis" %}">Cancelar</a>'),
          css_class='form-row d-flex',
        )
      )
    )

class EmpresaForm(forms.ModelForm):

  codigo = forms.CharField(disabled=True, required=False)
  dados_bancarios = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows":"5"}))
  endereco = forms.CharField(required=False)
  class Meta:
    model = Empresa
    fields = "__all__"

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_class = ''
    self.helper.layout = Layout(
      Row(
          Column('codigo', css_class='form-control-sm col-sm-2'),
          Column('nome', css_class='form-control-sm col-sm-8'),
          css_class='form-row d-flex',
      ),
      Row(
        Column('cnpj', css_class='form-control-sm col-lg-6'),
        Column('cidade',css_class='form-control-sm col-sm-4'),
        Column('estado',css_class='form-control-sm col-sm-2'),
        css_class='form-row d-flex',
      ),
      Row(
          Column('telefone', css_class='form-control-sm col-sm-4'),
          Column('endereco', css_class='form-control-sm col-sm-6'),
          Column('imposto', css_class='form-control-sm col-sm-2'),
          css_class='form-row d-flex',
      ),
      Row(
          Column('dados_bancarios', css_class='form-control-sm col-sm-8'),
          css_class='form-row d-flex',
      ),
      Div(
        Row(
          Submit('submit', 'Confirmar', css_class='mx-2'),
          HTML('<a class="btn btn-danger" href="{% url "empresas" %}">Cancelar</a>'),
          css_class='form-row d-flex',
          )
      )
    )

class NewEmpresaForm(EmpresaForm):

  codigo = forms.CharField(disabled=False, required=True)

class ServicosForm(forms.ModelForm):

  tipo = forms.ChoiceField(
    choices=Servicos.getTipos(),
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )

  class Meta:
      model = Servicos
      fields = "__all__"
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_class = ''
    self.helper.layout = Layout(
      Row(
        Column('codigo', css_class='form-control-sm col-sm-2'),
        Column('descricao', css_class='form-control-sm col-sm-6'),
        Column('versao', css_class='form-control-sm col-sm-2'),
        css_class='form-row d-flex',
      ),
      Row(
        Column('cliente', css_class='form-control-sm col-sm-2'),
        Column('nomeCliente', css_class='form-control-sm col-sm-6'),
        Column('tipo',css_class='form-control-sm col-sm-4'),
        css_class='form-row d-flex',
      ),
      Row(
        Column('observacao',css_class='form-control-sm col-sm-6'),
        css_class='form-row d-flex',
      ),
      Div(
        Row(
          Submit('submit', 'Confirmar', css_class='mx-2'),
          HTML('<a class="btn btn-danger" href="{% url "servicos" %}">Cancelar</a>'),
          css_class='form-row d-flex',
        )
      )
    )

class ProjetoForm(forms.ModelForm):

  codigo = forms.CharField(disabled=True, required=False)

  data_inicio = forms.DateField(
    required=False,
    widget=forms.TextInput(attrs={"class": "form-control", "type": "date"})
  )
  data_entrega = forms.DateField(
    required=False,
    widget=forms.TextInput(attrs={"class": "form-control", "type": "date"})
  )

  status = forms.ChoiceField(
    choices=Projetos.getStatus(),
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )

  desenvolvedor = forms.CharField(required=False)
  arquiteto = forms.CharField(required=False)

  class Meta:
    model = Projetos
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_class = 'border p-12'
    self.helper.layout = Layout(
      Row(
          Column('codigo', css_class='form-control-sm col-sm-2 mb-2 p-2'),
          Column('name', css_class='form-control-sm col-sm-6 mb-2 p-2'),
          Column('status', css_class='form-control-sm col-lg-3 mb-2 p-2'),
          css_class='form-row d-flex',
      ),
      Row(
        Column('cliente',css_class='form-control-sm col-sm-6 mb-2 p-2'),
        Column('responsavel',css_class='form-control-sm col-sm-4 mb-2 p-2'),
        css_class='form-row d-flex',
      ),
      Row(
          Column('data_inicio', css_class='form-control-sm col-sm-2 mb-0 p-2'),
          Column('data_entrega', css_class='form-control-sm col-sm-2 mb-0 p-2'),
          Column('desenvolvedor', css_class='form-control-sm col-sm-4 mb-0 p-2'),
          Column('arquiteto', css_class='form-control-sm col-sm-4 mb-0 p-2'),
          css_class='form-row d-flex',
      ),
      Row(
        Column('qtd_horas_projeto', css_class='form-control-sm col-sm-2 mb-0 p-2'),
        Column('qtd_horas_apontadas', css_class='form-control-sm col-sm-2 mb-0 p-2'),
        Column('valor_hora', css_class='form-control-sm col-sm-2 mb-0 p-2'),
        Column('valor_total', css_class='form-control-sm col-sm-2 mb-0 p-2'),
        css_class='form-row d-flex',
      ),
      Div(
        Row(
          Submit('submit', 'Confirmar', css_class='mt-3 mx-2'),
          HTML('<a class="btn btn-danger mt-3" href="{% url "projetos" %}">Cancelar</a>'),
          css_class='form-row d-flex',
          )
      )
    )

class NewProjetoForm(forms.ModelForm):
  class Meta:
    model = Projetos
    fields = '__all__'

  codigo = forms.CharField(
    label='Codigo do Projeto',
    required=True,
    widget = forms.TextInput(
      attrs={
        "placeholder": "ERP-0001",
      })
  )
  
  name = forms.CharField(
    label='Descrição',
    required=True,
  )

  data_inicio = forms.DateField(
    input_formats='%d-%m-%Y',
    required=False,
    widget = forms.TextInput(
      attrs={
        "type": "date",
      })
  )
  
  data_entrega = forms.DateField(
    input_formats='%d-%m-%Y',
    required=False,
    widget = forms.TextInput(
      attrs={
        "type": "date"
      })
  )

  qtd_horas_apontadas = forms.DecimalField(
    max_digits=4, 
    decimal_places=2, 
    required=False,
    label="Horas Apontadas",
  )
  
  qtd_horas_projeto = forms.DecimalField(
    max_digits=4, 
    decimal_places=2, 
    required=False,
    label="Horas do Projeto",
  )

  valor_hora = forms.DecimalField(
    localize=True, 
    required=False,
    label="Valor Hora",
  )
  
  valor_total = forms.DecimalField(
    localize=True, 
    required=False,
    label="Valor Total"
  )
  
  desenvolvedor = forms.ModelChoiceField(
    queryset=Usuario.objects.all(),
    to_field_name='name',
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )
  
  arquiteto = forms.ModelChoiceField(
    queryset=Usuario.objects.all().filter(tipo="1"),
    to_field_name='name',
    required=False,
    widget=forms.Select(attrs={'class': 'form-control'})
  )
  
  responsavel = forms.ModelChoiceField(
    queryset=Usuario.objects.all(),
    to_field_name='name',
    required=False,
    widget=forms.Select(attrs={'class': 'form-control'})
  )
  
  cliente = forms.ModelChoiceField(
    queryset=Cliente.objects.all(),
    to_field_name='name',
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )
  
  status = forms.ChoiceField(
    choices=Projetos.getStatus(),
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_class = 'border p-12'
    self.helper.layout = Layout(
      Row(
          Column('codigo', css_class='form-control-sm col-sm-2 mb-2 p-2'),
          Column('name', css_class='form-control-sm col-sm-6 mb-2 p-2'),
          Column('status', css_class='form-control-sm col-sm-3 mb-2 p-2'),
          css_class='form-row d-flex',
      ),
      Row(
        Column('cliente',css_class='form-control-sm col-sm-6 mb-2 p-2'),
        Column('responsavel',css_class='form-control-sm col-sm-4 mb-2 p-2'),
        css_class='form-row d-flex',
      ),
      Row(
          Column('data_inicio', css_class='form-control-sm col-sm-2 mb-0 p-2'),
          Column('data_entrega', css_class='form-control-sm col-sm-2 mb-0 p-2'),
          Column('desenvolvedor', css_class='form-control-sm col-sm-4 mb-0 p-2'),
          Column('arquiteto', css_class='form-control-sm col-sm-4 mb-0 p-2'),
          css_class='form-row d-flex',
      ),
      Row(
        Column('qtd_horas_projeto', css_class='form-control-sm col-sm-2 mb-0 p-2'),
        Column('qtd_horas_apontadas', css_class='form-control-sm col-sm-2 mb-0 p-2'),
        Column('valor_hora', css_class='form-control-sm col-sm-2 mb-0 p-2'),
        Column('valor_total', css_class='form-control-sm col-sm-2 mb-0 p-2'),
        css_class='form-row d-flex',
      ),
      Div(
        Row(
          Submit('submit', 'Confirmar', css_class='mt-3 mx-2'),
          HTML('<a class="btn btn-danger mt-3" href="{% url "projetos" %}">Cancelar</a>'),
          css_class='form-row d-flex',
          )
      )
    )
  