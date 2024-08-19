from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

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
  
  data_inicio = forms.DateField(
      widget=forms.TextInput(attrs={"class": "form-control", "type": "date"})
  )
  data_entrega = forms.DateField(
      widget=forms.TextInput(attrs={"class": "form-control", "type": "date"})
  )

  class Meta:
    model = Projetos
    fields = (
        "name",
        "cliente",
        "responsavel",
        "arquiteto",
        "data_inicio",
        "data_entrega",
        "desenvolvedor",
        "status",
    )

class NewProjetoForm(forms.ModelForm):
  
  codigo = forms.CharField(disabled=False)
  data_inicio = forms.DateField(
      widget=forms.TextInput(attrs={"class": "form-control", "type": "date"})
  )
  data_entrega = forms.DateField(
      widget=forms.TextInput(attrs={"class": "form-control", "type": "date"})
  )

  class Meta:
    model = Projetos
    fields = (
        "codigo",
        "name",
        "cliente",
        "responsavel",
        "arquiteto",
        "data_inicio",
        "data_entrega",
        "desenvolvedor",
        "status",
    )
