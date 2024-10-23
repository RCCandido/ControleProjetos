from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper 
from crispy_forms.layout import Layout, Submit, Row
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *

from .models import Usuario, Empresa, Servicos, Grupos, ItemGrupo, Cliente, Colaborador, Valores, ItemServico

class RedefinirSenhaForm(forms.ModelForm):
  email = forms.CharField(label="E-mail", disabled=True, required=False)
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

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_class = 'form-control'
    self.helper.label_class = 'm-0 p-0'
    self.helper.layout = Layout(
      Div(
        Row(
          Column('email', css_class='col-sm-8'),
          css_class='form-row d-flex',
        ),
        Row(
          Column('password', css_class='col-sm-4'),
          Column('password2', css_class='col-sm-4'),
          css_class='form-row d-flex',
        ),
        css_class="form-control"
      )
    )

class UsuarioForm(forms.ModelForm):

  def clean(self):
   super(UsuarioForm, self).clean()
  
   if 'password' in self.cleaned_data and 'password2' in self.cleaned_data:
     if self.cleaned_data['password'] != self.cleaned_data['password2']:
       raise ValidationError("As senhas não conferem.") 

  email = forms.EmailField(disabled=True)

  password = forms.CharField(
    label="Senha",
    widget=forms.PasswordInput(), 
    disabled=False, 
    required=False
  )

  password2 = forms.CharField(
    label="Repita a Senha",
    widget=forms.PasswordInput(), 
    disabled=False, 
    required=False
  )

  tipo = forms.ChoiceField(
    choices=Usuario.getTipos(),
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )
  
  perfil = forms.ModelChoiceField(
    queryset=Grupos.objects.all().order_by("descricao"),
    to_field_name='codigo',
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )

  class Meta:
    model = Usuario
    fields = (
        "firstname",
        "name",
        "email",
        "active",
        "tipo",
        "perfil",
        "usefilter",
        "resetpsw",
    )

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['name'].widget.attrs['class'] = 'my_class'
    self.helper = FormHelper()
    self.helper.form_class = 'form-control'
    self.helper.label_class = 'm-0 p-0'
    self.helper.layout = Layout(
      Row(
        Field('firstname', wrapper_class='col-sm-3'),
        Field('name', wrapper_class='col-sm-6'),
        css_class='form-row d-flex',
      ),
      Row(
        Field('email', wrapper_class='col-sm-6'),
        Field('tipo', wrapper_class='col-sm-2'),
        Field('perfil', wrapper_class='col-sm-2'),
        css_class='form-row d-flex',
      ),
      Row(
        Field('password', wrapper_class='col-sm-2'),
        Field('password2', wrapper_class='col-sm-2'),
        css_class='form-row d-flex',
      ),
      Row(
        Field('resetpsw', wrapper_class='form-control-sm'),
        Field('active', wrapper_class='form-control-sm'),
        Field('usefilter', wrapper_class='form-control-sm'),
        css_class='form-row d-flex',
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
 
class GruposForm(forms.ModelForm):

  class Meta:
      model = Grupos
      fields = "__all__"

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_class = 'form-control'
    self.helper.label_class = 'm-0 p-0'
    self.helper.layout = Layout(
      Div(
        Row(
          Column('descricao', css_class='col-sm-6'),
          css_class='form-row d-flex',
        ),
        Row(
          Column('active', css_class='form-control-sm'),
          css_class='form-row d-flex',
        ),
        css_class="form-control"
      )
    )

class ItemGrupoForm(forms.ModelForm):

  rotina = forms.ChoiceField(
    choices=ItemGrupo.getRotinas(),
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )
  
  inclusao = forms.ChoiceField(
    choices=Grupos.getSimNao(),
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )
  
  edicao = forms.ChoiceField(
    choices=Grupos.getSimNao(),
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )
  
  exclusao = forms.ChoiceField(
    choices=Grupos.getSimNao(),
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )
  
  logs = forms.ChoiceField(
    choices=Grupos.getSimNao(),
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )
  
  filtro = forms.ChoiceField(
    choices=Grupos.getSimNao(),
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )

  class Meta:
    model = ItemGrupo
    fields = "__all__"

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_class = 'form-control'
    self.helper.label_class = 'm-0 p-0'
    self.helper.layout = Layout(
      Row(
        Column('rotina', css_class='col-sm-6'),
        css_class='form-row d-flex',
      ),
      Row(
        Column('inclusao', css_class='col-sm-3'),
        Column('edicao', css_class='col-sm-3'),
        Column('exclusao', css_class='col-sm-3'),
        css_class='form-row d-flex',
      ),
      Row(
        Column('logs',css_class='col-sm-4'),
        Column('filtro',css_class='col-sm-4'),
        css_class='form-row d-flex',
      ),
    )

class EmpresaForm(forms.ModelForm):

  def validaPercent(value):
    if value > 100:
        raise ValidationError(
            _("%(value)s não é valido."),
            params={"value": value},
        )

  dados_bancarios = forms.CharField(
    required=False, 
    label="Dados Bancários",
    widget=forms.Textarea(
      attrs={
        "rows":"5",
        "placeholder": "Informações bancárias"
        }
      )
    )

  endereco = forms.CharField(
    required=False,
    label="Endereço",
    widget = forms.TextInput(
      attrs={
        'placeholder': "Av. da Esquina",
      })
    )
  
  estado = forms.ChoiceField(
    choices=Empresa.getUF(),
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )

  telefone = forms.CharField(
    required=False,
    label='Telefone',
    widget = forms.TextInput(
      attrs={
        'data-mask': "(99) 99999-9999",
        'placeholder': "(99) 99999-9999",
      })
    )
  
  cnpj = forms.CharField(
    required=False,
    max_length=18,
    label='CNPJ',
    widget = forms.TextInput(
      attrs={
        'data-mask': "99.999.999/9999-99",
        'placeholder': "99.999.999/9999-99",
      })
    )

  imposto = forms.DecimalField(
    required=False,
    label="% Imposto",
    widget=forms.NumberInput(
      attrs={
        'placeholder':"% 0.00",
        'step': '0.01',
        }
      )
    )

  class Meta:
    model = Empresa
    fields = "__all__"
    

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_class = 'form-control'
    self.helper.label_class = 'm-0 p-0'
    self.helper.layout = Layout(
      Row(
          Column('nome', css_class='col-sm-6'),
          Column('cnpj', css_class='col-lg-6'),
          css_class='form-row d-flex',
      ),
      Row(
          Column('endereco', css_class='col-sm-6'),
          Column('complemento',css_class='col-sm-4'),
          css_class='form-row d-flex',
      ),
      Row(
          Column('cep',css_class='col-sm-3'),
          Column('cidade',css_class='col-sm-3'),
          Column('estado',css_class='col-sm-2'),
          Column('telefone', css_class='col-sm-3'),
          css_class='form-row d-flex',
      ),
     
    )

class NewEmpresaForm(EmpresaForm):

  codigo = forms.CharField(disabled=False, required=True)

class ServicosForm(forms.ModelForm):

  codigo = forms.CharField(
    label='Codigo',
    disabled=False,
    required=True,
  )

  cliente = forms.ModelChoiceField(
    queryset=Cliente.objects.all().filter(active="1"),
    to_field_name='codigo',
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )

  tipo = forms.ChoiceField(
    choices=Servicos.getTipos(),
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )
  
  etapa_comercial = forms.ChoiceField(
    choices=Servicos.getEtapasComercial(),
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )
  
  etapa_tecnica = forms.ChoiceField(
    choices=Servicos.getEtapasTecnicas(),
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )

  justificativa = forms.CharField(
    required=False, 
    label="Justificativa", 
    widget=forms.Textarea(
      attrs={
        "rows":"5"
        })
  )
  
  anotacoes = forms.CharField(
    required=False, 
    label="Anotações", 
    widget=forms.Textarea(
      attrs={
        "rows":"5"
        })
  )

  versao = forms.CharField(
    initial="001",
    label='Versão',
    required=True,
    widget = forms.TextInput(
      attrs={
        'data-mask':"000"
      })
  )
  
  versao_valida = forms.CharField(
    initial="001",
    label='Versão Válida',
    required=False,
    widget = forms.TextInput(
      attrs={
        'data-mask':"000"
      })
  )
  
  class Meta:
    model = Servicos
    fields = "__all__"
    widgets = {
      'valor_hora': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'R$ 120.00'}),
      'comissao': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '10.00'}),
      'valor_comissao': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'R$ 10.00'}),
      'base_comissao': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'R$ 10.00'}),
      'imposto': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '2.50'}),
      'valor_imposto': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'R$ 25.00'}),
      'desconto': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '2.50'}),
      'valor_desconto': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'R$ 25.00'}),
      'valor_recebido': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'R$ 25.00'}),
      'custo_operacional': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'R$ 25.00'}),
      'valor_bruto': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'R$ 25,000.00'}),
      'liquido': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'R$ 25,000.00'}),
      'horas_especificacao': forms.NumberInput(attrs={'step': '0.10', 'placeholder': '00'}),
      'horas_tecnicas': forms.NumberInput(attrs={'step': '0.10', 'placeholder': '00'}),
      'horas_save': forms.NumberInput(attrs={'step': '0.10', 'placeholder': '00'}),
      'horas_execucao': forms.NumberInput(attrs={'step': '0.15', 'placeholder': '00'}),
    }
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_class = 'form-control'
    self.helper.label_class = 'm-0 p-0'
    self.helper.layout = Layout(
      Row(
        Field('codigo', wrapper_class='col-sm-2'),
        Field('tipo', wrapper_class='col-sm-2'),
        Field('versao', wrapper_class='col-sm-1'),
        css_class='form-row d-flex',
      ),
      Row(
        Field('descricao', wrapper_class='col-sm-6'),
        Field('cliente', wrapper_class='col-sm-6'),
        css_class='form-row d-flex',
      ),
      Row(
        Column('etapa_comercial',css_class='col-sm-4'),
        Column('etapa_tecnica',css_class='col-sm-4'),
        css_class='form-row d-flex',
      ),
      Row(
        Column('valor_hora',css_class='col-sm-2'),
        Column('valor_comissao',css_class='col-sm-2'),
        Column('comissao',css_class='col-sm-2'),
        Column('base_comissao',css_class='col-sm-2'),
        css_class='form-row d-flex',
      ),
      Row(
        Column('imposto',css_class='col-sm-2'),
        Column('valor_imposto',css_class='col-sm-2'),
        Column('desconto',css_class='col-sm-2'),
        Column('valor_desconto',css_class='col-sm-2'),
        Column('parcelas',css_class='col-sm-1'),
        css_class='form-row d-flex',
      ),
      Row(
        Column('custo_operacional',css_class='col-sm-3'),
        Column('horas_save',css_class='col-sm-2'),
        Column('horas_execucao',css_class='col-sm-2'),
        Column('horas_especificacao',css_class='col-sm-2'),
        Column('horas_tecnicas',css_class='col-sm-2'),
        css_class='form-row d-flex',
      ),
      Row(
        Column('valor_bruto',css_class='col-sm-3'),
        Column('liquido',css_class='col-sm-3'),
        Column('valor_recebido',css_class='col-sm-3'),
        css_class='form-row d-flex',
      ),
    )

class ItemServicoForm(forms.ModelForm):

  item = forms.CharField(
    label='Item',
    disabled=False,
    required=True,
  )

  tipo = forms.ChoiceField(
    choices=Servicos.getTipos(),
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )
  
  class Meta:
    model = ItemServico
    fields = (
      "item",
      "descricao_item",
      "sub_item",
      "descricao_sub_item",
      "tipo",
      "horas",
      "save",
      "execucao",
    )

    widgets = {
      'horas': forms.NumberInput(attrs={'step': '0.15', 'placeholder': '00'}),
      'save': forms.NumberInput(attrs={'step': '0.15', 'placeholder': '00'}),
      'execucao': forms.NumberInput(attrs={'step': '0.15', 'placeholder': '00'}),
    }
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_class = 'form-control'
    self.helper.layout = Layout(
      Row(
        Column('item', css_class='col-sm-2'),
        Column('descricao_item', css_class='col-sm-8'),
        css_class='form-row d-flex',
      ),
      Row(
        Column('sub_item', css_class='col-sm-2'),
        Column('descricao_sub_item', css_class='col-sm-8'),
        css_class='form-row d-flex',
      ),
      Row(
        Column('tipo',css_class='col-sm-5'),
        Column('horas',css_class='col-sm-4'),
        css_class='form-row d-flex',
      ),
      Row(
        Column('save',css_class='col-sm-4'),
        Column('execucao',css_class='col-sm-4'),
        css_class='form-row d-flex',
      ),
    )
  
class ClienteForm(forms.ModelForm):

  cnpj = forms.CharField(
    required=True,
    max_length=18,
    label='CNPJ',
    widget = forms.TextInput(
      attrs={
        'data-mask': "99.999.999/9999-99",
        'placeholder': "99.999.999/9999-99",
      })
    )

  estado = forms.ChoiceField(
    choices=Empresa.getUF(),
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )
 
  usa_email_cat = forms.ChoiceField(
    choices=Grupos.getSimNao(),
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )

  email_cat = forms.CharField(label='E-mail CAT', required=False)
  usa_email_cat = forms.ChoiceField(
    choices=Grupos.getSimNao(),
    required=True,
    label='CAT por e-mail?',
    widget=forms.Select(attrs={'class': 'form-control'})
  )
  
  dados_bancarios = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows":"5", "placeholder":"Dados para movimentações financeiras.."}))
  observacoes = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows":"5"}))
  contatos = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows":"5"}))

  
  class Meta:
    model = Cliente
    fields = "__all__"
    widgets = {
      'valor_hora_atual': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'R$ 120.00'}),
      'perc_desconto_atual': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '10.00'}),
    }

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_class = 'form-control'
    self.helper.label_class = 'm-0 p-0'
    self.helper.layout = Layout(
      Row(
        Column('nome', css_class='col-sm-6'),
        Column('cnpj', css_class='col-sm-3'),
        css_class='form-row d-flex m-0',
      ),
      Row(
        Column('ie', css_class='col-sm-2'),
        Column('telefone', css_class='col-sm-2'),
        Column('email', css_class='col-sm-4'),
        css_class='form-row d-flex m-0',
      ),
      Row(
        Column('endereco', css_class='col-sm-5'),
        Column('complemento',css_class='col-sm-3'),
        Column('cep',css_class='col-sm-2'),
        css_class='form-row d-flex m-0',
      ),
      Row(
        Column('bairro',css_class='col-sm-2'),
        Column('cidade',css_class='col-sm-2'),
        Column('estado', css_class='col-sm-2'),
        Column('usa_email_cat', css_class='col-sm-2'),
        Column('email_cat', css_class='col-sm-4'),
        css_class='form-row d-flex m-0',
      ),
      Row(
        Column('valor_hora_atual', css_class='col-sm-2'),
        Column('perc_desconto_atual',css_class='col-sm-2'),
        css_class='form-row d-flex m-0',
      ),
      Row(
        Column('active', css_class='m-0 p-0'),
        css_class='form-row d-flex m-0',
      ),
    )

class ColaboradorForm(forms.ModelForm):

  nome = forms.CharField(
    label='Nome Completo',
    required=True,
  )
  
  cpf = forms.CharField(
    label='CPF',
    required=True,
    widget = forms.TextInput(
      attrs={
        "placeholder": "999.999.999-99",
      })
  )

  estado = forms.ChoiceField(
    choices=Empresa.getUF(),
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'})
  )
  
  dados_bancarios = forms.CharField(
    required=False, 
    widget=forms.Textarea(
      attrs={
        "rows":"5", 
        "placeholder":"Dados para movimentações financeiras"
      })
  )

  funcao = forms.ChoiceField(
    choices=Colaborador.getFuncao(),
    required=True,
    label='Função',
    widget=forms.Select(attrs={'class': 'form-control'})
  )

  class Meta:
    model = Colaborador
    fields = "__all__"
    widgets = {
      'valor_hora': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'R$ 120.00'}),
      'valor_fixo': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'R$ 120.00'}),
      'comissao': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '10.00'}),
      'periodo_lancamento': forms.DateInput(
        attrs={
          'format': "dd/mm/yyyy",
          'placeholder': "dd/mm/yyyy",
          }),
    }

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_class = 'form-control'
    self.helper.label_class = 'm-0 p-0'
    self.helper.layout = Layout(
      Row(
        Column('nome', css_class='col-sm-6'),
        Column('active', css_class='my-4'),
        css_class='form-row d-flex',
      ),
      Row(
        Column('email', css_class='col-sm-4'),
        Column('cpf', css_class='col-sm-3'),
        Column('funcao', css_class='col-sm-3'),
        css_class='form-row d-flex',
      ),
      Row(
        Column('endereco', css_class='col-sm-4'),
        Column('complemento', css_class='col-sm-4'),
        Column('cep', css_class='col-sm-3'),
        css_class='form-row d-flex',
      ),
      Row(
        Column('bairro',css_class='col-sm-3'),
        Column('cidade',css_class='col-sm-3'),
        Column('estado', css_class='col-sm-2'),
        Column('telefone', css_class='col-sm-3'),
        css_class='form-row d-flex',
      ),
      Row(
        Column('periodo_lancamento',css_class='col-sm-3'),
        Column('valor_hora', css_class='col-sm-2'),
        Column('valor_fixo',css_class='col-sm-2'),
        Column('comissao',css_class='col-sm-2'),
        css_class='form-row d-flex',
      ),
    )

class ValoresForm(forms.ModelForm):

  codigo = forms.CharField(
    required=False,
  )

  tipo = forms.ChoiceField(
    choices=Valores.getTipos(),
    required=False,
    widget=forms.Select(attrs={'class': 'form-control'})
  )

  observacao = forms.CharField(
    label="Observações", 
    required=False, 
    widget=forms.Textarea(
      attrs={
        "rows":"5"
        }
      )
    )
  
  data = forms.DateField(
    required=False, 
    widget=forms.DateInput(
      format='%Y-%m-%d',
      attrs={
        'type': 'date',
      }),
      input_formats=('%Y-%m-%d',),
  )
  
  class Meta:
    model = Valores
    fields = "__all__"
    widgets = {
      'valor_hora': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'R$ 120.00'}),
      'valor_fixo': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'R$ 120.00'}),
      'desconto': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'R$ 120.00'}),
      'imposto': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '% 2.50'}),
      'comissao': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '% 2.50'}),
     
    }

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_class = 'form-control'
    self.helper.layout = Layout(
      Row(
        Column('tipo', css_class='col-sm-3'),
        Column('data', css_class='col-sm-3'),
        Column('active', css_class='col-sm-4 my-4'),
        css_class='form-row d-flex',
      ),
      Row(
        Column('valor_hora', css_class='col-sm-2'), 
        Column('valor_fixo',css_class='col-sm-2'),
        Column('comissao',css_class='col-sm-2'),
        Column('imposto',css_class='col-sm-2'),
        Column('desconto',css_class='col-sm-2'),
        css_class='form-row d-flex',
      ),
      Row(
        Column('observacao',css_class='col-sm-5'),
        css_class='form-row d-flex',
      ),
      Div(
        Row(
          Submit('submit', 'Confirmar', css_class='mx-2 mt-2'),
          HTML('<a class="btn btn-danger mt-2" href="{% url "valores" %}">Cancelar</a>'),
          css_class='form-row d-flex',
        )
      )
    )

