import random
import decimal 

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse 
from django.shortcuts import get_object_or_404
from datetime import datetime

from .models import Usuario, Empresa, Servicos, Niveis
from .forms import (
    UsuarioForm,
    NewUsuarioForm,
    EmpresaForm,
    ServicosForm,
    NivelForm,
    RedefinirSenhaForm,
    NewEmpresaForm,
    Cliente,
    ClienteForm,
    Colaborador,
    ColaboradorForm,
    Valores,
    ValoresForm,
    ItemServico,
    ItemServicoForm,
)
from .decorators import nivel_access_required
from .filters import UsuarioFilter, ClienteFilter

## LOGIN ##
def logar_usuario(request):

  if request.method == "POST":
    email = request.POST["email"]
    password = request.POST["password"]
    usuario = authenticate(request, username=email, password=password)
    if usuario is not None:

      # se usuaro nao esta ativo
      if not usuario.active:
        error = "Usuário Bloqueado."
        form_login = AuthenticationForm()
        return render(
            request,
            "projects/index.html",
            {"error": error, "form_login": form_login},
        )
      else:
        login(request, usuario)

        if usuario.resetpsw:
            return redirect("redefinir_senha")
        else:
            return redirect("home")
    else:
      error = "Usuário ou Senha inválido(s)."
      form_login = AuthenticationForm()
      return render(
          request,
          "projects/index.html",
          {"error": error, "form_login": form_login},
      )
  else:
    error = ""
    form_login = AuthenticationForm()
    return render(
        request, "projects/index.html", {"error": error, "form_login": form_login}
    )

def recuperar_senha(request):
  sucess = False
  message = ""
  if request.method == "POST":

    destinatario = request.POST["email"]
    
    if destinatario:
        
        # verifica se o destinatario tem o email cadastrado
        user = Usuario.objects.filter(email=destinatario).first()
        if user:

          # cria nova senha aleatoria
          nova_senha = SenhaAleatoria()

          senha_criptografada = make_password(
            password=nova_senha, salt=None, hasher="pbkdf2_sha256"
          )

          user.password = senha_criptografada
          user.save()

          mensagem = "Olá " + user.name + " Sua nova senha é: " + nova_senha

          # envia email de recuperação de senha
          send_mail(
            "Recuperação de Senha",
            mensagem,
            "rodrigo.candido@alphaerp.com.br",
            [destinatario],
            fail_silently=False,
          )
          sucess = True
          message = "E-mail de recuperação enviado com Sucesso!"
          return render(
            request,
            "projects/recuperar_senha.html",
            {"sucess": sucess, "message": message},
          )
        else:
          sucess = False
          message = "E-mail inválido, não consta na base de dados."
          return render(
            request,
            "projects/recuperar_senha.html",
            {"sucess": sucess, "message": message},
          )

    else:
      sucess = False
      message = "E-mail inválido, não consta na base de dados."
      return render(
        request,
        "projects/recuperar_senha.html",
        {"sucess": False, "message": message},
      )

  else:
    return render(
      request,
      "projects/recuperar_senha.html",
      {"sucess": False, "message": ""},
    )

@login_required(login_url="/index")
def deslogar_usuario(request):
    logout(request)
    return redirect("home")

@login_required(login_url="/index")
def redefinir_senha(request):
    form = RedefinirSenhaForm(instance=request.user)

    if request.method == "POST":
        novasenha = request.POST["password"]
        novasenha2 = request.POST["password2"]

        if novasenha != novasenha2:
            erro = "As senhas não conferem."
            return render(
                request, "projects/redefinir_senha.html", {"form": form, "erro": erro}
            )
        else:
            user = Usuario.objects.filter(email=request.user.email).first()
            if user:
                user.set_password(novasenha)
                message = "Senha alterada com sucesso! Será necessário realizar um novo login com a sua nova senha."
                return render(
                    request,
                    "projects/logoff.html",
                    {"message": message, "type": "success"},
                )

    return render(request, "projects/redefinir_senha.html", {"form": form, "erro": ""})

## MENUS ##
@login_required(login_url="/index")
def home(request):
  return render(request, "projects/home.html")

@login_required(login_url="/index")
@nivel_access_required(view_name="usuarios")
def usuarios(request, opc=False, pk=False):
  
  if request.method == "POST":
    
    if opc == "insert":

      form = NewUsuarioForm(request.POST)
      if form.is_valid():

        usuario = Usuario(
          firstname = form.cleaned_data["firstname"],
          name      = form.cleaned_data["name"],
          email     = form.cleaned_data["email"],
          password  = make_password(form.cleaned_data["password"]),
          password2 = make_password(form.cleaned_data["password2"]),
          active    = form.cleaned_data["active"],
          tipo      = form.cleaned_data["tipo"],
          perfil    = form.cleaned_data["perfil"],
          usefilter = form.cleaned_data["usefilter"],
        )
        usuario.save()

        return redirect("usuarios")

      else:
        return render(
          request,
          "projects/usuarios.html",
          {"inclui": True, "form": form},
        )

    elif opc == "edit":
      
      usuario = Usuario.objects.filter(email=pk).first()
      form = UsuarioForm(request.POST, instance=usuario)
      if form.is_valid():
        usuario = form.save(commit=False)
        usuario.firstname = form.cleaned_data["firstname"]
        usuario.name      = form.cleaned_data["name"]
        usuario.active    = form.cleaned_data["active"]
        usuario.tipo      = form.cleaned_data["tipo"]
        usuario.perfil    = form.cleaned_data["perfil"]
        usuario.usefilter = form.cleaned_data["usefilter"]
        usuario.save()
        return redirect("usuarios")
      else:
        return render(request,"projects/usuarios.html",{"altera": True, "form": form})
  else:
    if opc == "insert":
      form = NewUsuarioForm()
      context = {"inclui": True, "form": form}
      return render(request,"projects/usuarios.html", context)

    elif opc == "edit":
      if pk:
        usuario = Usuario.objects.filter(email=pk).first()
        form = UsuarioForm(instance=usuario)
        context = {"altera": True, "form": form}
        return render(request, "projects/usuarios.html", context)

    elif opc == "delete":
      if pk:
        usuario = Usuario.objects.filter(email=pk).first()

        if usuario:
          usuario.delete()

        users = Usuario.objects.all()
        filter = UsuarioFilter(request.GET, queryset=users)

        context = {"usuarios": filter, "filter": filter}
        return render(request, "projects/usuarios.html", context)

    users = Usuario.objects.all().order_by("user_id")
    filter = UsuarioFilter(request.GET, queryset=users)

    context = {"usuarios": filter, "filter": filter}
    return render(request, "projects/usuarios.html", context)

@login_required(login_url="/index")
@nivel_access_required(view_name="servicos")
def servicos(request, opc=False, pk=False):
  
  if request.method == "POST":
    
    if opc == "insert":

      form = ServicosForm(request.POST)
      if form.is_valid():
        
        codigo = Servicos.getNextCodigo()

        servico = Servicos(
          codigo      = codigo,
          descricao   = form.cleaned_data["descricao"],
          versao      = form.cleaned_data["versao"],
          cliente     = form.cleaned_data["cliente"],
          tipo        = form.cleaned_data["tipo"],
          valor_hora  = form.cleaned_data["valor_hora"],
          comissao    = form.cleaned_data["comissao"],
          imposto     = form.cleaned_data["imposto"],
          valor_imposto   = form.cleaned_data["valor_imposto"],
          horas_especificacao = form.cleaned_data["horas_especificacao"],
          horas_tecnicas  = form.cleaned_data["horas_tecnicas"],
          valor_bruto     = form.cleaned_data["valor_bruto"],
          desconto        = form.cleaned_data["desconto"],
          valor_desconto  = form.cleaned_data["valor_desconto"],
          valor_recebido  = form.cleaned_data["valor_recebido"],
          base_comissao   = form.cleaned_data["base_comissao"],
          valor_comissao  = form.cleaned_data["valor_comissao"],
          custo_operacional = form.cleaned_data["custo_operacional"],
          liquido         = form.cleaned_data["liquido"],
          horas_save      = form.cleaned_data["horas_save"],
          horas_execucao  = form.cleaned_data["horas_execucao"],
          etapa_comercial = form.cleaned_data["etapa_comercial"],
          etapa_tecnica   = form.cleaned_data["etapa_tecnica"],
          justificativa   = form.cleaned_data["justificativa"],
          anotacoes       = form.cleaned_data["anotacoes"],
          versao_valida   = form.cleaned_data["versao_valida"],
          parcelamento    = form.cleaned_data["parcelamento"],
        )
        servico.save()

        # insere o registro na tabela de valores
        valor = Valores(
          data = datetime.today,
          codigo = codigo,
          tipo = 'Servico',
          valor_hora = form.cleaned_data["valor_hora"],
          comissao = form.cleaned_data["comissao"],
          imposto = form.cleaned_data["imposto"],
          desconto = form.cleaned_data["desconto"],
        )
        valor.save()

        return redirect("servicos")

      else:
        return render(
          request,
          "projects/servicos.html",
          {
            "inclui": True,
            "form": form,
          },
        )

    elif opc == "edit":

      servico = Servicos.objects.filter(codigo=pk).first()
      form = ServicosForm(request.POST, instance=servico)
      if form.is_valid():
        form.save()
        #servico = form.save(commit=False)
        #servico.descricao   = form.cleaned_data["descricao"]
        #servico.descricao   = form.cleaned_data["descricao"],
        #servico.versao      = form.cleaned_data["versao"],
        #servico.tipo        = form.cleaned_data["tipo"],
        ##servico.comissao    = form.cleaned_data["comissao"],
        #servico.save()

        # insere o registro na tabela de valores
        valor = Valores(
          data = datetime.today,
          codigo = form.cleaned_data["codigo"],
          tipo = 'Servico',
          valor_hora = form.cleaned_data["valor_hora"],
          comissao = form.cleaned_data["comissao"],
          imposto = form.cleaned_data["imposto"],
          desconto = form.cleaned_data["desconto"],
        )
        valor.save()

        return redirect("servicos")
      else:
        return render(
          request,
          "projects/servicos.html",
          {"altera": True, "form": form, 'form_errors': form.errors},
        )

    elif opc == "item_add":
      form = ItemServicoForm(request.POST)
      if form.is_valid():
        form.save()
        return render(request, "projects/partials/success.html")
      return render(request, "projects/partials/failure.html")

    form_item = ItemServicoForm()
    context = {"form_item": form_item}
    return render(request, "projects/servicos.html", context)

  else:

    if opc == "insert":
      
      form = ServicosForm(initial={'codigo' : Servicos.getNextCodigo()})
      form_item = ItemServicoForm()

      context = {"inclui": True, "form": form, "form_item": form_item}
      return render(request, "projects/servicos.html", context)

    elif opc == "edit":
      if pk:

        servico = Servicos.objects.filter(codigo=pk).first()
        form = ServicosForm(instance=servico)
        items = ItemServico.objects.filter(codigo=pk)
        form_item = ItemServicoForm()
        
        context = {
          "altera": True, 
          "form": form,
          "items": items,
          "form_item": form_item,
          }
        return render(request, "projects/servicos.html", context)

    elif opc == "delete":
      if pk:
        servico = Servicos.objects.filter(codigo=pk).first()
        
        if servico:
          servico.delete()
        
        servicos = Servicos.objects.all()
        context = {"servicos": servicos}
        return render(request, "projects/servicos.html", context)

    else:
      servicos = Servicos.objects.all()
      context = {"servicos": servicos}
      return render(request, "projects/servicos.html", context)

def adicionar_item_servico(request):
  pk = request.GET.get('pk')
  object = get_object_or_404(ItemServico, pk = pk)
  form = ItemServicoForm(instance=object)
  return render(request, 'servicos.html', {
        'object': object,
        'pk': pk,
        'form_item': form,
        })


@login_required(login_url="/index")
@nivel_access_required(view_name="empresas")
def empresas(request, pk=False, opc=False):
  
  if request.method == "POST":
    
    if opc == "insert":
    
      form = EmpresaForm(request.POST, prefix="form")
      form_valores = ValoresForm(request.POST, prefix="form_valores")
      if form.is_valid() and form_valores.is_valid():

        empresa = Empresa(
          nome            = form.cleaned_data["nome"],
          cnpj            = form.cleaned_data["cnpj"],
          endereco        = form.cleaned_data["endereco"],
          cidade          = form.cleaned_data["cidade"],
          estado          = form.cleaned_data["estado"],
          telefone        = form.cleaned_data["telefone"],
          dados_bancarios = form.cleaned_data["dados_bancarios"],
          imposto         = form.cleaned_data["imposto"],
        )
        empresa.save()
        
        if form.cleaned_data["imposto"] > 0:
            
          # insere o registro na tabela de valores
          valor = Valores(
            data = form_valores.cleaned_data["data"],
            codigo = empresa.codigo,
            tipo = 'Empresa',
            imposto = form.cleaned_data["imposto"],
            observacao = form_valores.cleaned_data["observacao"],
          )
          valor.save()

        return redirect("empresas")

      else:
        return render(
            request,
            "projects/empresas.html",
            {"inclui": True, "form": form, "form_valores": form_valores},
        )

    elif opc == "edit":
        
      empresa = Empresa.objects.filter(codigo=pk).first()
      impostoAnterior = empresa.imposto

      form = EmpresaForm(request.POST, instance=empresa, prefix="form")
      form_valores = ValoresForm(request.POST, prefix="form_valores")
      if form.is_valid() and form_valores.is_valid():

        registraValor = True if form.cleaned_data["imposto"] != impostoAnterior else False

        empresa = form.save(commit=False)
        empresa.nome            = form.cleaned_data["nome"]
        empresa.cnpj            = form.cleaned_data["cnpj"]
        empresa.endereco        = form.cleaned_data["endereco"]
        empresa.cidade          = form.cleaned_data["cidade"]
        empresa.estado          = form.cleaned_data["estado"]
        empresa.telefone        = form.cleaned_data["telefone"]
        empresa.dados_bancarios = form.cleaned_data["dados_bancarios"]
        empresa.imposto         = form.cleaned_data["imposto"]
        empresa.save()

        if registraValor:

          # insere o registro na tabela de valores
          valor = Valores(
            data = form_valores.cleaned_data["data"],
            codigo = empresa.codigo,
            tipo = 'Empresa',
            imposto = form.cleaned_data["imposto"],
            observacao = form_valores.cleaned_data["observacao"],
          )
          valor.save()

        return redirect("empresas")

      else:
        context = {
          "altera": True,
          "form": form,
          "form_valores": form_valores
          }
        return render(request, "projects/empresas.html", context)
  else:

    if opc == "insert":
      form = NewEmpresaForm(prefix="form")
      form_valores = ValoresForm(prefix="form_valores", initial={'data': datetime.today})

      context = {
        "inclui": True,
        "form": form,
        "form_valores": form_valores
        }
      return render(request, "projects/empresas.html", context)

    elif opc == "edit":
      if pk:
        empresa = Empresa.objects.filter(codigo=pk).first()
        form = EmpresaForm(instance=empresa, prefix="form")
        form_valores = ValoresForm(prefix="form_valores", initial={'data': datetime.today})
        historico = Valores.objects.filter(codigo=pk, tipo="Empresa").order_by("-valor_id")

        context = {
          "altera": True, 
          "form": form,
          "form_valores": form_valores,
          "historico": historico,
          }
        return render(request, "projects/empresas.html", context)

    elif opc == "delete":
      if pk:
        empresa = Empresa.objects.filter(codigo=pk).first()
        
        if empresa:
          empresa.delete()

        empresas = Empresa.objects.all()
        
        context = {"empresa": empresas}
        return render(request, "projects/empresas.html", context)

    empresas = Empresa.objects.all()
    context = {"empresa": empresas}
    return render(request, "projects/empresas.html", context)
          
@login_required(login_url="/index")
@nivel_access_required(view_name="niveis")
def niveis(request, pk=False, opc=False):

  if request.method == "POST":
    if opc == "insert":

      form = NivelForm(request.POST)
      if form.is_valid():

        nivel = Niveis(
            descricao = form.cleaned_data["descricao"],
            rotina    = form.cleaned_data["rotina"],
            inclusao  = form.cleaned_data["inclusao"],
            edicao    = form.cleaned_data["edicao"],
            exclusao  = form.cleaned_data["exclusao"],
            logs      = form.cleaned_data["logs"],
            filtro    = form.cleaned_data["filtro"],
            active    = form.cleaned_data["active"],
        )
        nivel.save()

        return redirect("niveis")

      else:
        context = {"inclui": True, "form": form}
        return render(request, "projects/niveis.html", context,)
        
    elif opc == "edit":

      nivel = Niveis.objects.filter(nivel_id=pk).first()
      form = NivelForm(request.POST, instance=nivel)
      if form.is_valid():
        
        nivel = form.save(commit=False)
        nivel.descricao = form.cleaned_data["descricao"]
        nivel.rotina    = form.cleaned_data["rotina"]
        nivel.inclusao  = form.cleaned_data["inclusao"]
        nivel.edicao    = form.cleaned_data["edicao"]
        nivel.exclusao  = form.cleaned_data["exclusao"]
        nivel.logs      = form.cleaned_data["logs"]
        nivel.filtro    = form.cleaned_data["filtro"]
        nivel.active    = form.cleaned_data["active"]
        nivel.save()

        return redirect("niveis")
      else:
        context = {"inclui": True, "form": form}
        return render(request, "projects/niveis.html", context)
  else:

    if opc == "insert":
      nivel_form = NivelForm()
      context = {"inclui": True, "form": nivel_form}
      return render(request, "projects/niveis.html", context)

    elif opc == "edit":
      if pk:
        nivel = Niveis.objects.filter(nivel_id=pk).first()
        form = NivelForm(instance=nivel)
        context = {"altera": True, "form": form}
        return render(request, "projects/niveis.html", context)

    elif opc == "delete":
      if pk:
        nivel = Niveis.objects.filter(nivel_id=pk).first()
        
        if nivel:
          nivel.delete()

        niveis = Niveis.objects.all()
        context = {"niveis": niveis}
        return render(request, "projects/niveis.html", context)

    niveis = Niveis.objects.all()
    context = {"niveis": niveis}
    return render(request, "projects/niveis.html", context)

@login_required(login_url="/index")
def clientes(request, opc=False, pk=False):
  
  if request.method == "POST":
    
    if opc == "insert":

      form = ClienteForm(request.POST, prefix="form")
      form_valores = ValoresForm(request.POST, prefix="form_valores")
      if form.is_valid() and form_valores.is_valid():

        cliente = Cliente(
          nome               = form.cleaned_data["nome"],
          cnpj               = form.cleaned_data["cnpj"],
          ie                 = form.cleaned_data["ie"],
          endereco           = form.cleaned_data["endereco"],
          complemento        = form.cleaned_data["complemento"],
          bairro             = form.cleaned_data["bairro"],
          cidade             = form.cleaned_data["cidade"],
          estado             = form.cleaned_data["estado"],
          email              = form.cleaned_data["email"],
          email_cat          = form.cleaned_data["email_cat"],
          usa_email_cat      = form.cleaned_data["usa_email_cat"],
          telefone           = form.cleaned_data["telefone"],
          contatos           = form.cleaned_data["contatos"],
          dados_bancarios    = form.cleaned_data["dados_bancarios"],
          observacoes        = form.cleaned_data["observacoes"],
          valor_hora_atual   = form.cleaned_data["valor_hora_atual"],
          perc_desconto_atual= form.cleaned_data["perc_desconto_atual"],
          active             = form.cleaned_data["active"],
        )
        cliente.save()

        if form.cleaned_data["perc_desconto_atual"] > 0 or form.cleaned_data["valor_hora_atual"] > 0:

          # insere o registro na tabela de valores
          valor = Valores(
            data = form_valores.cleaned_data["data"],
            codigo = cliente.codigo,
            tipo = 'Cliente',
            valor_hora = form.cleaned_data["valor_hora_atual"],
            desconto = form.cleaned_data["perc_desconto_atual"],
            observacao = form_valores.cleaned_data["observacao"],
          )
          valor.save()

        return redirect("clientes")

      else:
        context = {
          "inclui": True,
          "form": form, 
          "form_valores": form_valores,
          }

        return render(request, "projects/clientes.html", context)

    elif opc == "edit":
      
      cliente = Cliente.objects.filter(codigo=pk).first()
      valorHoraAnterior = cliente.valor_hora_atual
      descontoAnterior = cliente.perc_desconto_atual
      registraValor = False
      
      form = ClienteForm(request.POST, instance=cliente, prefix="form")
      form_valores = ValoresForm(request.POST, prefix="form_valores")
      if form.is_valid() and form_valores.is_valid():
        
        registraValor = True if valorHoraAnterior != form.cleaned_data["valor_hora_atual"] or descontoAnterior != form.cleaned_data["perc_desconto_atual"] else False
        
        cliente = form.save(commit=False)
        cliente.nome                = form.cleaned_data["nome"]
        cliente.cnpj                = form.cleaned_data["cnpj"]
        cliente.ie                  = form.cleaned_data["ie"]
        cliente.endereco            = form.cleaned_data["endereco"]
        cliente.complemento         = form.cleaned_data["complemento"]
        cliente.bairro              = form.cleaned_data["bairro"]
        cliente.cidade              = form.cleaned_data["cidade"]
        cliente.estado              = form.cleaned_data["estado"]
        cliente.email               = form.cleaned_data["email"]
        cliente.email_cat           = form.cleaned_data["email_cat"]
        cliente.usa_email_cat       = form.cleaned_data["usa_email_cat"]
        cliente.telefone            = form.cleaned_data["telefone"]
        cliente.contatos            = form.cleaned_data["contatos"]
        cliente.dados_bancarios     = form.cleaned_data["dados_bancarios"]
        cliente.observacoes         = form.cleaned_data["observacoes"]
        cliente.valor_hora_atual    = form.cleaned_data["valor_hora_atual"]
        cliente.perc_desconto_atual = form.cleaned_data["perc_desconto_atual"]
        cliente.active              = form.cleaned_data["active"]
        cliente.save()

        if registraValor:

          # insere o registro na tabela de valores
          valor = Valores(
            data = form_valores.cleaned_data["data"],
            codigo = cliente.codigo,
            tipo = 'Cliente',
            valor_hora = form.cleaned_data["valor_hora_atual"],
            desconto = form.cleaned_data["perc_desconto_atual"],
            observacao = form_valores.cleaned_data["observacao"],
          )
          valor.save()

        return redirect("clientes")

      else:
        context = {
          "altera": True,
          "form": form,
          "form_valores": form_valores,
          }
        return render(request, "projects/clientes.html", context)
  else:

    if opc == "insert":
      form = ClienteForm(prefix="form")
      form_valores = ValoresForm(prefix="form_valores", initial={'data': datetime.today})

      context = {
        "inclui": True, 
        "form": form,
        "form_valores": form_valores,
        }
      return render(request, "projects/clientes.html", context)

    elif opc == "edit":
      if pk:
        cliente = Cliente.objects.filter(codigo=pk).first()
        form = ClienteForm(instance=cliente, prefix="form")
        form_valores = ValoresForm(prefix="form_valores", initial={'data': datetime.today})
        historico = Valores.objects.filter(codigo=pk, tipo="Cliente").order_by("-valor_id")

        context = {
          "altera": True, 
          "form": form,
          "form_valores": form_valores,
          "historico": historico,
        }
        return render(request, "projects/clientes.html", context)

    elif opc == "delete":
      if pk:
        cliente = Cliente.objects.filter(codigo=pk).first()
        
        if cliente:
          cliente.delete()

        clientes = Cliente.objects.all()
        filter = ClienteFilter(request.GET, queryset=clientes)
        
        context = {
            "cliente": clientes,
            "filter": filter,
          }
        return render(request, "projects/clientes.html", context)

    clientes = Cliente.objects.all()
    filter = ClienteFilter(request.GET, queryset=clientes)

    context = {
        "clientes": filter,
        "filter": filter,
      }
    return render(request, "projects/clientes.html", context)

@login_required(login_url="/index")
def colaboradores(request, opc=False, pk=False):
  
  if request.method == "POST":
   
    if opc == "insert":

      form = ColaboradorForm(request.POST, prefix="form")
      form_valores = ValoresForm(request.POST, prefix="form_valores")
      if form.is_valid() and form_valores.is_valid():

        colaborador = Colaborador(
          nome               = form.cleaned_data["nome"],
          cpf                = form.cleaned_data["cpf"],
          endereco           = form.cleaned_data["endereco"],
          bairro             = form.cleaned_data["bairro"],
          cidade             = form.cleaned_data["cidade"],
          estado             = form.cleaned_data["estado"],
          email              = form.cleaned_data["email"],
          telefone           = form.cleaned_data["telefone"],
          dados_bancarios    = form.cleaned_data["dados_bancarios"],
          valor_hora         = form.cleaned_data["valor_hora"],
          valor_fixo         = form.cleaned_data["valor_fixo"],
          comissao           = form.cleaned_data["comissao"],
          funcao             = form.cleaned_data["funcao"],
          active             = form.cleaned_data["active"],
          periodo_lancamento = form.cleaned_data["periodo_lancamento"],
        )
        colaborador.save()

        # insere o registro na tabela de valores
        valor = Valores(
          data = form_valores.cleaned_data["data"],
          codigo = colaborador.codigo,
          tipo = 'Colaborador',
          valor_fixo = form.cleaned_data["valor_fixo"],
          valor_hora = form.cleaned_data["valor_hora"],
          comissao = form.cleaned_data["comissao"],
          observacao = form_valores.cleaned_data["observacao"],
        )
        valor.save()

        return redirect("colaboradores")

      else:
        context = {
          "inclui": True,
          "form": form,
          "form_valores": form_valores,
          }
        return render(request,"projects/colaboradores.html", context)

    elif opc == "edit":
        
      colaborador = Colaborador.objects.filter(codigo=pk).first()
      valorHoraAnterior = colaborador.valor_hora
      valorFixoAnterior = colaborador.valor_fixo
      comissaoAnterior = colaborador.comissao
      registraValor = False

      form = ColaboradorForm(request.POST, instance=colaborador, prefix="form")
      form_valores = ValoresForm(request.POST, prefix="form_valores")
      if form.is_valid() and form_valores.is_valid():

        if valorHoraAnterior != form.cleaned_data["valor_hora"] or valorFixoAnterior != form.cleaned_data["valor_fixo"] or comissaoAnterior != form.cleaned_data["comissao"]:
          registraValor = True
            
        colaborador.nome               = form.cleaned_data["nome"]
        colaborador.cpf                = form.cleaned_data["cpf"]
        colaborador.endereco           = form.cleaned_data["endereco"]
        colaborador.bairro             = form.cleaned_data["bairro"]
        colaborador.cidade             = form.cleaned_data["cidade"]
        colaborador.estado             = form.cleaned_data["estado"]
        colaborador.email              = form.cleaned_data["email"]
        colaborador.telefone           = form.cleaned_data["telefone"]
        colaborador.dados_bancarios    = form.cleaned_data["dados_bancarios"]
        colaborador.valor_hora         = form.cleaned_data["valor_hora"]
        colaborador.valor_fixo         = form.cleaned_data["valor_fixo"]
        colaborador.comissao           = form.cleaned_data["comissao"]
        colaborador.funcao             = form.cleaned_data["funcao"]
        colaborador.active             = form.cleaned_data["active"]
        colaborador.periodo_lancamento = form.cleaned_data["periodo_lancamento"]
        colaborador.save()

        if registraValor:

          # insere o registro na tabela de valores
          valor = Valores(
            data = form_valores.cleaned_data["data"],
            codigo = colaborador.codigo,
            tipo = 'Colaborador',
            valor_hora = form.cleaned_data["valor_hora"],
            valor_fixo = form.cleaned_data["valor_fixo"],
            comissao = form.cleaned_data["comissao"],
            observacao = form_valores.cleaned_data["observacao"],
          )
          valor.save()

        return redirect("colaboradores")
      else:
        context = {
          "altera": True,
          "form": form,
          "form_valores": form_valores,
          }
        return render(request,"projects/colaboradores.html", context)

  else:

    if opc == "insert":
      form = ColaboradorForm(prefix="form")
      form_valores = ValoresForm(prefix="form_valores", initial={'data': datetime.today})

      context = {
        "inclui": True,
        "form": form,
        "form_valores": form_valores,
        }
      return render(request, "projects/colaboradores.html", context)

    elif opc == "edit":
      if pk:
        colaborador = Colaborador.objects.filter(codigo=pk).first()
        form = ColaboradorForm(instance=colaborador, prefix="form")
        form_valores = ValoresForm(prefix="form_valores", initial={'data': datetime.today})
        historico = Valores.objects.filter(codigo=pk, tipo="Colaborador").order_by("-valor_id")

        context = {
          "altera": True,
          "form": form,
          "form_valores": form_valores,
          "historico": historico,
          }
        return render(request, "projects/colaboradores.html", context)

    elif opc == "delete":
      if pk:
        colaborador = Colaborador.objects.filter(codigo=pk).first()

        if colaborador:
          colaborador.delete()

        colaboradores = Colaborador.objects.all()
        context = {"colaborador": colaboradores}
        return render(request, "projects/colaboradores.html", context)

    colaboradores = Colaborador.objects.all()
    context = {"colaboradores": colaboradores}
    return render(request, "projects/colaboradores.html", context)

@login_required(login_url="/index")
def valores(request, opc=False, pk=False):
  
  if request.method == "POST":
   
    form = ValoresForm(request.POST)

    if form.is_valid():

      data        = form.cleaned_data["data"]
      valor_hora  = form.cleaned_data["valor_hora"]
      valor_fixo  = form.cleaned_data["valor_fixo"]
      comissao    = form.cleaned_data["comissao"]
      imposto     = form.cleaned_data["imposto"]
      desconto    = form.cleaned_data["desconto"]
      active      = form.cleaned_data["active"]
      observacao  = form.cleaned_data["observacao"]

      if opc == "insert":

        valores = Valores(
          data       = data,
          valor_hora = valor_hora,
          valor_fixo = valor_fixo,
          comissao   = comissao,
          imposto    = imposto,
          desconto   = desconto,
          active     = active,
          observacao = observacao,
        )

        valores.save()

        return redirect("valores")

      elif opc == "edit":
        
        valores = Valores.objects.filter(codigo=pk).first()

        valores.data       = data
        valores.valor_hora = valor_hora
        valores.valor_fixo = valor_fixo
        valores.comissao   = comissao
        valores.imposto    = imposto
        valores.desconto   = desconto
        valores.active     = active
        valores.observacao = observacao
        
        valores.save()

        return redirect("valores")
    else:
      return render(
          request,
          "projects/valores.html",
          {"form": form, "altera": True},
      )
  else:

    if opc == "insert":
      form = ValoresForm()
      context = {"inclui": True, "form": form}
      return render(request, "projects/valores.html", context)

    elif opc == "edit":
      if pk:
        valores = Valores.objects.filter(codigo=pk).first()
        form = ValoresForm(instance=valores)
        context = {"altera": True, "form": form}
        return render(request, "projects/valores.html", context)

    elif opc == "delete":
      if pk:
        valores = Valores.objects.filter(codigo=pk).first()
        
        if valores:
          valores.delete()

        valores = Valores.objects.all()
        context = {"valores": valores}
        return render(request, "projects/valores.html", context)

    else:
      valores = Valores.objects.all()
      context = {"valores": valores}
      return render(request, "projects/valores.html", context)

@login_required(login_url="/index")
def relatorios(request):
    context = {
        "type": "primary",
        "title": "Relatórios",
        "message": "Página em construção.",
    }
    return render(request, "projects/em_construcao.html", context)

@login_required(login_url="/index")
def profile(request):
    context = {
        "type": "primary",
        "title": "Profile",
        "message": "Página em construção.",
    }
    return render(request, "projects/em_construcao.html", context)


@login_required(login_url="/index")
def logs(request):
    context = {
        "type": "primary",
        "title": "Logs",
        "message": "Página em construção.",
    }
    return render(request, "projects/em_construcao.html", context)


############ DASHBOARD ############
def retorna_total_usuarios(request):
  # total = Usuario.objects.all().aggregate(Sum('total'))['total__sum']
  total = Usuario.objects.all().count()
  return JsonResponse({'total_usuarios': total})

def retorna_total_projetos(request):
  x = Usuario.objects.all()

  data = []
  labels = []
  mes = datetime.now().month + 1
  ano = datetime.now().year
  meses = (
      [
        "Jan",
        "Fev",
        "Mar",
        "Abr",
        "Mai",
        "Jun",
        "Jul",
        "Ago",
        "Set",
        "Out",
        "Nov",
        "Dez",
      ],
  )

  for i in range(12):
    mes -= 1
    if mes == 0:
        mes = 12
        ano -= 1

    y = sum([i.valor_total for i in x if i.data_inicio.month == mes and i.data_inicio.year == ano])
    labels.append(meses[mes-1])
    data.append(y)

  data_json = {'data': data[::-1], 'labels': labels[::-1]}

  return JsonResponse(data_json)

############ functions ############
def isInt(value):
  try:
    int(value)
    return True
  except:
    return False


def SenhaAleatoria():
  numero = random.randrange(100000, 999999)
  return str(numero)


def cargainicial(request):

  niveis = [
      {"descricao": "Nivel 1"},
      {"descricao": "Nivel 2"},
      {"descricao": "Nivel 3"},
    ]

  users = [
      {"nome": "rodrigo", "email": "rodrigo.cesar91@yahoo.com.br"},
      {"nome": "velton", "email": "velton@alphaerp.com.br"},
      {"nome": "joao", "email": "joao@alphaerp.com.br"},
    ]

  clientes = [
      {"nome": "Unimed Participações", "cnpj": "123456789", "telefone": "98045036","email":"emailteste.com.br", "estado":"PR"},
      {"nome": "Grupo AIZ LTDA", "cnpj": "123456789", "telefone": "98045036","email":"emailteste.com.br", "estado":"PR"},
    ]

  servicos = [
      {"codigo": "SV0001", "descricao": "Serviço de Teste 1", "tipo": "Pontual"},
      {"codigo": "SV0002", "descricao": "Serviço 002", "tipo": "Sustentação"},
      {"codigo": "SERV01", "descricao": "Serviço para Testar", "tipo": "Projeto"},
    ]

  empresas = [
    {"codigo": "EMP001", "nome": "ALPHA ERP", "cnpj": "07876633951", "cidade": "Curitiba", "estado": "PR", "telefone": "41998044063", "imposto": 2},
    {"codigo": "EMP002", "nome": "Administradora", "cnpj": "0732312456", "cidade": "Curitiba", "estado": "RJ", "telefone": "41998044063", "imposto": 10},
  ]

  if Niveis.objects.all().count() == 0:
    for i in niveis:
      nivel = Niveis(
              descricao=i['descricao'],
              rotina="0",
              inclusao="S",
              edicao="S",
              exclusao="S",
              logs="S",
              filtro="S",
              active=True
          )
      nivel.save()

    if not Usuario.objects.all().count():
      for i in users:
        user = Usuario(
            firstname=i['nome'].capitalize(),
            name=i['nome'].capitalize(),
            email=i['email'],
            password=make_password("123"),
            password2=make_password("123"),
            active=True,
            tipo="2",
            perfil=nivel,
            resetpsw=0,
        )
        user.save()

  if not Cliente.objects.all().count():
    for i in clientes:
      cliente = Cliente(
          nome               = i['nome'],
          cnpj               = i['cnpj'],
          estado             = i['estado'],
          email              = i['email'],
          usa_email_cat      = "S",
          telefone           = i['telefone'],
          active             = True,
        )
      cliente.save()
  
  
  #for i in servicos:
  #  servico = Servicos(
  #    descricao= i['descricao'],
  #    versao="001", 
  #    cliente=cliente,
  #    tipo= i['tipo'],
  #  )
  #  servico.save()
  
  if not Empresa.objects.all().count():
    for i in empresas:
      empresa = Empresa(
        nome            = i['nome'],
        cnpj            = i['cnpj'],
        cidade          = i['cidade'],
        estado          = i['estado'],
        telefone        = i['telefone'],
        imposto         = i['imposto'],
      )
      empresa.save()

  return redirect("home")
