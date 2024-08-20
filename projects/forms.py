from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML, Div

from .models import Usuario, Empresa, Servicos, Niveis, Projetos


class NewUsuarioForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(), required=True, label="Senha"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(), required=True, label="Repita a Senha"
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
            "resetpsw",
            "usefilter",
        )


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

  email = forms.CharField(disabled=True, required=False)
  password = forms.CharField(
      widget=forms.PasswordInput(), disabled=True, required=False
  )
  password2 = forms.CharField(
      widget=forms.PasswordInput(), disabled=True, required=False
  )

  perfil = forms.ModelChoiceField(
      queryset=Niveis.objects.all().order_by("descricao"),
      widget=forms.Select,
      required=True,
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
      )

  # def __init__(self, *args, **kwargs):
  #  super(Niveis, self).__init__(*args, **kwargs)
  #  self.fields['descricao'].queryset = Niveis.objects.all()


class NivelForm(forms.ModelForm):
  class Meta:
      model = Niveis
      fields = (
          "descricao",
          "rotina",
          "inclusao",
          "edicao",
          "exclusao",
          "logs",
          "filtro",
          "active",
      )

      # Uni-form
      helper = FormHelper()
      helper.form_class = "form-horizontal"
      helper.layout = Layout(
          Field("text_input", css_class="input-xlarge"),
          Field("textarea", rows="3", css_class="input-xlarge"),
          "radio_buttons",
          Field("checkboxes", style="background: #FAFAFA; padding: 10px;"),
          AppendedText("appended_text", ".00"),
          PrependedText(
              "prepended_text",
              '<input type="checkbox" checked="checked" value="" id="" name="">',
              active=True,
          ),
          PrependedText("prepended_text_two", "@"),
          "multicolon_select",
          FormActions(
              Submit("save_changes", "Save changes", css_class="btn-primary"),
              Submit("cancel", "Cancel"),
          ),
      )


class EmpresaForm(forms.ModelForm):
  class Meta:
      model = Empresa
      fields = ("codigo", "nome")


class ServicosForm(forms.ModelForm):
  class Meta:
      model = Servicos
      fields = (
          "codigo",
          "descricao",
          "versao",
          "cliente",
          "nomeCliente",
          "tipo",
          "observacao",
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
          Column('name', css_class='form-control-sm col-md-6 mb-2 p-2'),
          Column('status', css_class='form-control-sm col-lg-2 mb-2 p-2'),
          css_class='form-row d-flex',
      ),
      Row(
        Column('cliente',css_class='form-control-sm col-md-6 mb-2 p-2'),
        Column('responsavel',css_class='form-control-sm col-md-4 mb-2 p-2'),
        css_class='form-row d-flex',
      ),
      Row(
          Column('data_inicio', css_class='form-control-sm col-md-2 mb-0 p-2'),
          Column('data_entrega', css_class='form-control-sm col-md-2 mb-0 p-2'),
          Column('desenvolvedor', css_class='form-control-sm col-md-4 mb-0 p-2'),
          Column('arquiteto', css_class='form-control-sm col-md-4 mb-0 p-2'),
          css_class='form-row d-flex',
      ),
      Row(
        Column('qtd_horas_projeto', css_class='form-control-sm col-md-2 mb-0 p-2'),
        Column('qtd_horas_apontadas', css_class='form-control-sm col-md-2 mb-0 p-2'),
        Column('valor_hora', css_class='form-control-sm col-md-2 mb-0 p-2'),
        Column('valor_total', css_class='form-control-sm col-md-2 mb-0 p-2'),
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
          Column('name', css_class='form-control-sm col-md-6 mb-2 p-2'),
          Column('status', css_class='form-control-sm col-lg-2 mb-2 p-2'),
          css_class='form-row d-flex',
      ),
      Row(
        Column('cliente',css_class='form-control-sm col-md-6 mb-2 p-2'),
        Column('responsavel',css_class='form-control-sm col-md-4 mb-2 p-2'),
        css_class='form-row d-flex',
      ),
      Row(
          Column('data_inicio', css_class='form-control-sm col-md-2 mb-0 p-2'),
          Column('data_entrega', css_class='form-control-sm col-md-2 mb-0 p-2'),
          Column('desenvolvedor', css_class='form-control-sm col-md-4 mb-0 p-2'),
          Column('arquiteto', css_class='form-control-sm col-md-4 mb-0 p-2'),
          css_class='form-row d-flex',
      ),
      Row(
        Column('qtd_horas_projeto', css_class='form-control-sm col-md-2 mb-0 p-2'),
        Column('qtd_horas_apontadas', css_class='form-control-sm col-md-2 mb-0 p-2'),
        Column('valor_hora', css_class='form-control-sm col-md-2 mb-0 p-2'),
        Column('valor_total', css_class='form-control-sm col-md-2 mb-0 p-2'),
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
  