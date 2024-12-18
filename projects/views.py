import random
import re

from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from datetime import datetime
from .models import Usuario, Empresa, Servicos, Grupos, ItemGrupo
from .forms import (
    UsuarioForm,
    NewUsuarioForm,
    EmpresaForm,
    ServicosForm,
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
    GruposForm,
    ItemGrupoForm,
)
from .decorators import nivel_access_required
from .filters import UsuarioFilter, ClienteFilter, GruposFilter, EmpresaFilter, ColaboradorFilter, ServicosFilter

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
          
          # verifica se nao está bloqueado
          if user.active:

            # cria nova senha aleatoria
            nova_senha = SenhaAleatoria()

            senha_criptografada = make_password(
              password=nova_senha, salt=None, hasher="pbkdf2_sha256"
            )

            user.password = senha_criptografada
            user.resetpsw = True
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

          else:
            sucess = False
            message = "Usuário bloqueado, solicite ativação de seu usuário ao administrador."

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
  
  # verifica se tem permissão da ação
  if opc:
    if not hasAccessOpc(opc=opc, rotina="3", user=request.user):
      messages.error(request, "Usuário sem permissão para esta ação.")
      return redirect("usuarios")

  # envio submit POST
  if request.method == "POST":
    
    # se operação de criação
    if opc == "insert":
      
      # instancio o formulario enviado
      form = NewUsuarioForm(request.POST)

      # se válido
      if form.is_valid():
        
        # cria um novo usuario
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

    # se operação de edição de um usuario
    elif opc == "edit":
      
      # instancia o id do usuario (email)
      usuario = Usuario.objects.filter(email=pk).first()

      # instancia o formulario do usuario passado
      form = UsuarioForm(request.POST, instance=usuario)

      # se válido
      if form.is_valid():

        # salva as alterações no usuario posicionado
        usuario = form.save(commit=False)
        usuario.firstname = form.cleaned_data["firstname"]
        usuario.name      = form.cleaned_data["name"]
        usuario.active    = form.cleaned_data["active"]
        usuario.tipo      = form.cleaned_data["tipo"]
        usuario.perfil    = form.cleaned_data["perfil"]
        usuario.usefilter = form.cleaned_data["usefilter"]
        usuario.save()

        # se for o proprio usuario se desativando, desloga o mesmo
        if not usuario.active and usuario.email == request.user.email:
          deslogar_usuario(request)

        return redirect("usuarios")

      else:
        return render(request,"projects/usuarios.html",{"altera": True, "form": form})
  
  # se não for um SUBMIT de um form
  else:

    # e opção é de visualização
    if opc == "view":
      
      # recupera o usuario do id passado via parametro
      usuario = Usuario.objects.filter(email=pk).first()

      # cria um formulario instaciado como usuario
      form = UsuarioForm(instance=usuario)

      # monta o contexto para o template
      context = {"visualiza": True, "form": form}
      return render(request, "projects/usuarios.html", context)

    # e opção é de inserção de um novo usuario
    elif opc == "insert":
      
      # verifica permissao do grupo
      itemGrupo = ItemGrupo.objects.filter(grupo_id=request.user.perfil_id, rotina="3").first()

      # se nao tem um perfil ou nao permite
      if not itemGrupo or itemGrupo.inclusao == "N":
        messages.error(request, "Usuário sem acesso para Inclusão.")
        return redirect("usuarios")

      # cria um formulario para um novo usuario
      form = NewUsuarioForm()

      # monta o contexto para renderizar no template
      context = {"inclui": True, "form": form}
      return render(request,"projects/usuarios.html", context)

    # se for para edição de um usuario existente
    elif opc == "edit":
      
      # verifica permissao do grupo
      itemGrupo = ItemGrupo.objects.filter(grupo_id=request.user.perfil_id, rotina="3").first()

      # se nao tem um perfil ou nao permite
      if not itemGrupo or itemGrupo.edicao == "N":
        messages.error(request, "Usuário sem acesso para Edição.")
        return redirect("usuarios")

      # valida se foi enviado o id
      if pk:

        # recupera o usuario do id passado via parametro
        usuario = Usuario.objects.filter(email=pk).first()

        # cria um formulario instaciado como usuario
        form = UsuarioForm(instance=usuario)

        # monta o contexto para o template
        context = {"altera": True, "form": form}
        return render(request, "projects/usuarios.html", context)

    # se for operação de exclusão do usuario
    elif opc == "delete":
      
      # verifica permissao do grupo
      itemGrupo = ItemGrupo.objects.filter(grupo_id=request.user.perfil_id, rotina="3").first()

      # se nao tem um perfil ou nao permite
      if not itemGrupo or itemGrupo.exclusao == "N":
        messages.error(request, "Usuário sem acesso para Exclusão.")
        return redirect("usuarios")

      # valida se foi enviado o ID a ser excluido
      if pk:

        # instancia o usuario pelo id
        usuario = Usuario.objects.filter(email=pk).first()

        # se usuario válido, exclui
        if usuario:
          usuario.delete()


  # carrega a lista de usuarios existentes
  users = Usuario.objects.all().order_by("user_id")

  # monta o filtro
  filter = UsuarioFilter(request.GET, queryset=users)

  # monta o contexto para o template
  context = {"usuarios": filter, "filter": filter}
  return render(request, "projects/usuarios.html", context)

@login_required(login_url="/index")
@nivel_access_required(view_name="servicos")
def servicos(request, opc=False, pk=False):
  
  # verifica se tem permissão da ação
  if opc:
    if not hasAccessOpc(opc=opc, rotina="5", user=request.user):
      messages.error(request, "Usuário sem permissão para esta ação.")
      return redirect("servicos")

  if request.method == "POST":
    
    if opc == "insert":

      form = ServicosForm(request.POST)
      if form.is_valid():
        
        servico = Servicos(
          codigo      = form.cleaned_data["codigo"],
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
          parcelas        = form.cleaned_data["parcelas"],
        )
        servico.save()

        # insere o registro na tabela de valores
        valor = Valores(
          data = datetime.now(),
          codigo = servico.codigo,
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
        #valor = Valores(
        #  data = datetime.today,
        #  codigo = form.cleaned_data["codigo"],
        #  tipo = 'Servico',
        #  valor_hora = form.cleaned_data["valor_hora"],
        #  comissao = form.cleaned_data["comissao"],
        #  imposto = form.cleaned_data["imposto"],
        #  desconto = form.cleaned_data["desconto"],
        #)
        #valor.save()

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

    if opc == "view":
      
      if pk:

        servico = Servicos.objects.filter(codigo=pk).first()
        form = ServicosForm(instance=servico)
        items = ItemServico.objects.filter(codigo=pk)
        form_item = ItemServicoForm()
        
        context = {
          "visualiza": True, 
          "form": form,
          "items": items,
          "form_item": form_item,
          }
        return render(request, "projects/servicos.html", context)

    elif opc == "insert":
      
      # verifica permissao do grupo
      itemGrupo = ItemGrupo.objects.filter(grupo_id=request.user.perfil_id, rotina="5").first()

      # se nao tem um perfil ou nao permite
      if not itemGrupo or itemGrupo.inclusao == "N":
        messages.error(request, "Usuário sem acesso para Inclusão.")
        return redirect("servicos")

      form = ServicosForm(initial={'codigo' : Servicos.getNextCodigo()})
      form_item = ItemServicoForm()

      context = {"inclui": True, "form": form, "form_item": form_item}
      return render(request, "projects/servicos.html", context)

    elif opc == "edit":
      
      # verifica permissao do grupo
      itemGrupo = ItemGrupo.objects.filter(grupo_id=request.user.perfil_id, rotina="5").first()

      # se tem um perfil mas nao permite
      if itemGrupo and itemGrupo.edicao == "N":
        messages.error(request, "Usuário sem acesso para Edição.")
        return redirect("servicos")

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

    # busca toda a lista de servicos cadastrados
    servicos = Servicos.objects.all()
    
    # monta o filtro
    filter = ServicosFilter(request.GET, queryset=servicos)

    # contexto para o template
    context = {"servicos": filter, "filter": filter}
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
  
  # verifica se tem permissão da ação
  if opc:
    if not hasAccessOpc(opc=opc, rotina="1", user=request.user):
      messages.error(request, "Usuário sem permissão para esta ação.")
      return redirect("empresas")

  # se vindo de um submit
  if request.method == "POST":
    
    # se opção de inserção
    if opc == "insert":
      
      # obtem o formulario do POST
      form = EmpresaForm(request.POST, prefix="form")

      # obtem o form de valores do segundo POST
      form_valores = ValoresForm(request.POST, prefix="form_valores")

      # valida se estao validos
      if form.is_valid() and form_valores.is_valid():
        
        # instancia uma empresa nova
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

        # salva
        empresa.save()
        
        # se foi informado o imposto
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

      # formularios nao validos
      else:
        return render(
            request,
            "projects/empresas.html",
            {"inclui": True, "form": form, "form_valores": form_valores},
        )

    # se operação de alteração
    elif opc == "edit":
      
      # instancia a empresa com o ID passado
      empresa = Empresa.objects.filter(codigo=pk).first()

      # salva o imposto existente
      impostoAnterior = empresa.imposto

      # instancia a empresa do formulario postado
      form = EmpresaForm(request.POST, instance=empresa, prefix="form")

      # instancia o formulario de valores postado
      form_valores = ValoresForm(request.POST, prefix="form_valores")

      # se formularios validos
      if form.is_valid() and form_valores.is_valid():
        
        # verifica se os impostos sao diferentes
        registraValor = True if form.cleaned_data["imposto"] != impostoAnterior else False

        # instancia a empresa para alteração
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

        # se registra a alteração de valores
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

      # se formularios nao validos
      else:
        context = {
          "altera": True,
          "form": form,
          "form_valores": form_valores
          }
        return render(request, "projects/empresas.html", context)

  # se nao foi um post de formulario
  else:
    
     # e opção é de visualização
    if opc == "view":

      # se passado o id
      if pk:
      
        # filtra o id passado
        empresa = Empresa.objects.filter(codigo=pk).first()

        # instancia o formulario
        form = EmpresaForm(instance=empresa, prefix="form") 

        # instancia o formulario de item 
        form_valores = ValoresForm(prefix="form_valores")

        # instancia o grid de itens já cadastrados 
        historico = Valores.objects.filter(codigo=pk, tipo="Empresa").order_by("-valor_id")

        # monta o contexto para o template
        context = {
          "visualiza": True, 
          "form": form,
          "form_valores": form_valores,
          "historico": historico,
          }
        return render(request, "projects/empresas.html", context)

    # solicitada operação de criação de nova empresa
    elif opc == "insert":

      # insntancia um formulario de nova empresa
      form = NewEmpresaForm(prefix="form")

      # formulario para valores
      form_valores = ValoresForm(prefix="form_valores", initial={'data': datetime.today})

      context = {
        "inclui": True,
        "form": form,
        "form_valores": form_valores
        }
      return render(request, "projects/empresas.html", context)

    # solicitada tela de edição de empresa
    elif opc == "edit":

      # se enviado um ID para alteração
      if pk:

        # insntancia a empresa com o ID
        empresa = Empresa.objects.filter(codigo=pk).first()

        # insntancia um formuçario para alteração dessa empresa
        form = EmpresaForm(instance=empresa, prefix="form")

        # instancia um formulario para alteração de valores
        form_valores = ValoresForm(prefix="form_valores", initial={'data': datetime.today})

        # busca os valores pre-cadastrados para a empresa ordenando pelo id
        historico = Valores.objects.filter(codigo=pk, tipo="Empresa").order_by("-valor_id")

        context = {
          "altera": True, 
          "form": form,
          "form_valores": form_valores,
          "historico": historico,
          }
        return render(request, "projects/empresas.html", context)

    # se solicitada opção de exclusao de empresa
    elif opc == "delete":

      # se enviado o id para exclusao
      if pk:

        # busca a empresa do id passado
        empresa = Empresa.objects.filter(codigo=pk).first()
        
        # se encontrou a empresa
        if empresa:

          # apaga
          empresa.delete()

    # busca todas as empresas cadastradas para listagem no browse
    empresas = Empresa.objects.all()
    
    # monta o filtro
    filter = EmpresaFilter(request.GET, queryset=empresas)

    # monta o contexto para o template
    context = {"empresa": filter, "filter": filter}
    return render(request, "projects/empresas.html", context)

@login_required(login_url="/index")
@nivel_access_required(view_name="grupos")
def grupos(request, pk=False, opc=False, grupo=False):
  
  # verifica se tem permissão da ação
  if opc:
    if not hasAccessOpc(opc=opc, rotina="2", user=request.user):
      messages.error(request, "Usuário sem permissão para esta ação.")
      return redirect("grupos")

  if request.method == "POST":

    # se operação de insert vindo de um submit POST
    if opc == "insert":

      # instancia o formulario
      form = GruposForm(request.POST, prefix="form")
      
      # se válido
      if form.is_valid():
        
        # instancia um grupo com os dados passdos
        grupo = Grupos(
          descricao = form.cleaned_data["descricao"],
          active    = form.cleaned_data["active"],
        )
        grupo.save()
       
        return redirect("grupos")

      else:
        context = {
          "inclui": True, 
          "form": form,
          }
        return render(request, "projects/grupos.html", context)

    # se operação de edição de um grupo  
    elif opc == "edit":
      
      # filtra o grupo passado pelo id
      grupo = Grupos.objects.filter(codigo=pk).first()

      # instancia o forulario do grupo
      form = GruposForm(request.POST, instance=grupo, prefix="form")

      # se valido
      if form.is_valid():
        
        # commita o formulario salvando o grupo no banco
        grupo = form.save(commit=False)
        grupo.descricao = form.cleaned_data["descricao"]
        grupo.active    = form.cleaned_data["active"]
        grupo.save()

        return redirect("grupos")

      # se nao valido
      else:

        # monta o contexto para renderizar no template
        context = {
          "altera": True, 
          "form": form,
          "form_item": form_item,
          "msgerro": form_item.errors,
          }
        return render(request, "projects/grupos.html", context)
  
  # se nao for submit de formulario, mas para abrir a tela
  else:

    # e opção é de visualização
    if opc == "view":

      # se passado o id
      if pk:
      
        # filtra o id passado
        grupo = Grupos.objects.filter(codigo=pk).first()

        # instancia o formulario
        form = GruposForm(instance=grupo, prefix="form")

        # instancia o formulario de item 
        form_item = ItemGrupoForm(prefix="form_item")

        # instancia o grid de itens já cadastrados pelo grupo passado no id da url
        grid = ItemGrupo.objects.filter(grupo=pk)

        # monta o contexto para o template
        context = {
          "visualiza": True, 
          "form": form,
          "form_item": form_item,
          "grid": grid,
          }
        return render(request, "projects/grupos.html", context)

    # se operacao de insert 
    elif opc == "insert":
      form = GruposForm(prefix="form")

      context = {
        "inclui": True, 
        "form": form, 
        }
      return render(request, "projects/grupos.html", context)

    # se operacao de edição
    elif opc == "edit":

      # se passado o id
      if pk:

        # filtra o id passado
        grupo = Grupos.objects.filter(codigo=pk).first()

        # instancia o formulario para edição
        form = GruposForm(instance=grupo, prefix="form")

        # instancia o formulario de item 
        form_item = ItemGrupoForm(prefix="form_item")

        # instancia o grid de itens já cadastrados pelo grupo passado no id da url
        grid = ItemGrupo.objects.filter(grupo=pk)

        context = {
          "altera": True, 
          "form": form,
          "form_item": form_item,
          "grid": grid,
          }
        return render(request, "projects/grupos.html", context)

    # se clicado em deletar o grupo
    elif opc == "delete":

      # se passado o id
      if pk:

        # filtra (posiciona)
        grupo = Grupos.objects.filter(codigo=pk).first()
        
        # se encontrado o grupo
        if grupo:

          # apaga
          grupo.delete()

    # se clicado na operção de deletar um item dentro da edição de um grupo
    elif opc == "itemDelete":

      # monta a url para retornar depois da deleção
      url = "/grupos/edit/"+grupo

      # se passado um id de item para deleção
      if pk:

        # posiciona
        item = ItemGrupo.objects.filter(id=pk).first()
        
        # se encontrado o item
        if item:
          item.delete()

      return redirect(url)

    # caso nao seja passado nenhuma opção, busca a lista de grupos para exibição na tela principal
    grupos = Grupos.objects.all()

    # monta o filtro
    filter = GruposFilter(request.GET, queryset=grupos)

    # monta o contexto para o template
    context = {"grupos": filter, "filter": filter}
    return render(request, "projects/grupos.html", context)

def itemGrupo(request, pk=False, opc=False):
  
  # se vindo de submit do MODAL da pagina de grupos
  if request.method == "POST":

    #obtem o id do grupo no campo hidden do form
    pk = request.POST.get('pk') 

    #remove caracteres especais
    pk = re.sub('[^0-9]', '', pk) 

    # filtra o grupo
    grupo = Grupos.objects.filter(codigo=pk).first()

    # monta url de redirecionamento para a mesma pagina
    url = "/grupos/edit/"+pk

    # obtem o formulario do item (modal)
    form = ItemGrupoForm(request.POST, prefix="form_item")

    # se válido
    if form.is_valid() and grupo:
      
      # obtem o item para validar repetido
      itemGrupo = ItemGrupo.objects.filter(rotina=form.cleaned_data["rotina"], grupo_id=pk).first()
      if itemGrupo != None:
        messages.error(request, "Já existe a rotina cadastrada.")
        return redirect(url)

      # se o item válido, salva
      item = form.save(commit=False)
      item.grupo    = grupo
      item.rotina   = form.cleaned_data["rotina"]
      item.inclusao = form.cleaned_data["inclusao"]
      item.edicao   = form.cleaned_data["edicao"]
      item.exclusao = form.cleaned_data["exclusao"]
      item.logs     = form.cleaned_data["logs"]
      item.filtro   = form.cleaned_data["filtro"]
      item.save()
      
  return redirect(url)

@login_required(login_url="/index")
@nivel_access_required(view_name="clientes")
def clientes(request, opc=False, pk=False):
  
  # verifica se tem permissão da ação
  if opc:
    if not hasAccessOpc(opc=opc, rotina="4", user=request.user):
      messages.error(request, "Usuário sem permissão para esta ação.")
      return redirect("clientes")

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

    # e opção é de visualização
    if opc == "view":

      # se passado o id
      if pk:
      
        # filtra o id passado
        cliente = Cliente.objects.filter(codigo=pk).first()

        # instancia o formulario
        form = ClienteForm(instance=cliente, prefix="form") 

        # instancia o formulario de item 
        form_valores = ValoresForm(prefix="form_valores")

        # instancia o grid de itens já cadastrados 
        historico = Valores.objects.filter(codigo=pk, tipo="Cliente").order_by("-valor_id")

        # monta o contexto para o template
        context = {
          "visualiza": True, 
          "form": form,
          "form_valores": form_valores,
          "historico": historico,
        }
        return render(request, "projects/clientes.html", context)

    elif opc == "insert":
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
@nivel_access_required(view_name="colaboradores")
def colaboradores(request, opc=False, pk=False):
  
  # verifica se tem permissão da ação
  if opc:
    if not hasAccessOpc(opc=opc, rotina="6", user=request.user):
      messages.error(request, "Usuário sem permissão para esta ação.")
      return redirect("colaboradores")

  if request.method == "POST":
   
    if opc == "insert":

      form = ColaboradorForm(request.POST, prefix="form")
      form_valores = ValoresForm(request.POST, prefix="form_valores")
      if form.is_valid() and form_valores.is_valid():
        
        #valida o cpf
        if Colaborador.objects.filter(cpf = form.cleaned_data["cpf"]).first():
          
          msgerro = "Já existe um Colaborador com este CPF cadastrado."

          context = {
          "inclui": True,
          "form": form,
          "form_valores": form_valores,
          "msgerro": msgerro,
          }
          return render(request,"projects/colaboradores.html", context)

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

      form_valores = ValoresForm(request.POST, prefix="form_valores")
      form = ColaboradorForm(request.POST, instance=colaborador, prefix="form")
      if not form.is_valid():

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
          'msgerro': form.errors
        }
        return render(request,"projects/colaboradores.html", context)

  else:
    
     # e opção é de visualização
    if opc == "view":

      # se passado o id
      if pk:
      
        # filtra o id passado
        colaborador = Colaborador.objects.filter(codigo=pk).first()

        # instancia o formulario
        form = ColaboradorForm(instance=colaborador, prefix="form") 

        # instancia o formulario de item 
        form_valores = ValoresForm(prefix="form_valores")

        # instancia o grid de itens já cadastrados 
        historico = Valores.objects.filter(codigo=pk, tipo="Colaborador").order_by("-valor_id")

        # monta o contexto para o template
        context = {
          "visualiza": True, 
          "form": form,
          "form_valores": form_valores,
          "historico": historico,
          }
        return render(request, "projects/colaboradores.html", context)

    elif opc == "insert":
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


    # busca toda a lista de colaboradores cadastrados
    colaboradores = Colaborador.objects.all()
    
    # monta o filtro
    filter = ColaboradorFilter(request.GET, queryset=colaboradores)

    # contexto para o template
    context = {"colaboradores": filter, "filter": filter}
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
          resetpsw=False,
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


# Função que verifica se a Ação clicada é permitida ao usuário logado conforme o grupo
def hasAccessOpc(opc, rotina, user):
  
  # obtem o grupo do usuario
  grupo = ItemGrupo.objects.filter(grupo_id=user.perfil_id, rotina=rotina).first() 
  
  # se nao tem grupo, não permite nada
  if not grupo:
    return False

  # nao permite inserção
  if opc == "insert" and grupo.inclusao != "S":
    return False
  
  # nao permite edição
  if opc == "edit" and grupo.edicao != "S":
    return False
  
  # nao permite exclusão
  if opc == "delete" and grupo.exclusao != "S":
    return False

  return True