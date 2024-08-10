from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

from .models import Usuario, Empresa, Servicos, Niveis

class NewUsuarioForm(forms.ModelForm):
  class Meta:
    model = Usuario
    fields = (
              'name',
              'email',
              'password',
              'password2',
              'bloqueado',
              'tipo',
              'perfil',
            )
class UsuarioForm(forms.ModelForm):
  email = forms.CharField(disabled=True, required=False)
  password = forms.CharField(disabled=True, required=False)
  password2 = forms.CharField(disabled=True, required=False)
  class Meta:
    model = Usuario
    fields = (
              'name',
              'email',
              'password',
              'password2',
              'bloqueado',
              'tipo',
              'perfil',
            )
  
class NivelForm(forms.ModelForm):
  class Meta:
    model = Niveis
    fields = (
      'descricao',
      'rotina',
      'inclusao',
      'edicao',
      'exclusao',
      'logs',
      'filtro',
      'bloqueado'
      )
    
    # Uni-form
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('text_input', css_class='input-xlarge'),
        Field('textarea', rows="3", css_class='input-xlarge'),
        'radio_buttons',
        Field('checkboxes', style="background: #FAFAFA; padding: 10px;"),
        AppendedText('appended_text', '.00'),
        PrependedText('prepended_text', '<input type="checkbox" checked="checked" value="" id="" name="">', active=True),
        PrependedText('prepended_text_two', '@'),
        'multicolon_select',
        FormActions(
            Submit('save_changes', 'Save changes', css_class="btn-primary"),
            Submit('cancel', 'Cancel'),
        )
    )

class EmpresaForm(forms.ModelForm):
  class Meta:
    model = Empresa
    fields = ('codigo','nome')

class ServicosForm(forms.ModelForm):
  class Meta:
    model = Servicos
    fields = ('codigo','descricao','versao','cliente','nomeCliente','tipo','observacao')
