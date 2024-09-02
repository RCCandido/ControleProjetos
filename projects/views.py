import random

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse 
from datetime import datetime

from .models import Usuario, Empresa, Servicos, Niveis, Projetos
from .forms import (
    UsuarioForm,
    NewUsuarioForm,
    EmpresaForm,
    ServicosForm,
    NivelForm,
    RedefinirSenhaForm,
    ProjetoForm,
    NewProjetoForm,
    NewEmpresaForm,
    Cliente,
    ClienteForm,
    Colaborador,
    ColaboradorForm,
    Valores,
    ValoresForm,
)
from .decorators import nivel_access_required
from .filters import UsuarioFilter, ProjetoFilter

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
    
    form = UsuarioForm(request.POST)
    if form.is_valid():
      
      firstname = form.cleaned_data["firstname"]
      name      = form.cleaned_data["name"]
      active    = form.cleaned_data["active"]
      tipo      = form.cleaned_data["tipo"]
      perfil    = form.cleaned_data["perfil"]
      usefilter = form.cleaned_data["usefilter"]

      if opc == "insert":
        
        user = Usuario(
          firstname = firstname,
          name      = name,
          email     = form.cleaned_data["email"],
          password  = make_password(form.cleaned_data["password"]),
          password2 = make_password(form.cleaned_data["password2"]),
          active    = active,
          tipo      = tipo,
          perfil    = perfil,
          usefilter = usefilter,
        )
        user.save()

      elif opc == "edit":

        usuario = Usuario.objects.filter(email=pk).first()

        usuario.firstname = firstname
        usuario.name      = name
        usuario.active    = active
        usuario.tipo      = tipo
        usuario.perfil    = perfil
        usuario.usefilter = usefilter
        usuario.save()

        return redirect("usuarios")
    else:
      erro = form.errors
      return render(
          request,
          "projects/usuarios.html",
          {"altera": True, "form": form, "erro": erro},
      )

  else:
    if opc == "insert":
      form = NewUsuarioForm()
      context = {"inclui": True, "form": form}
      return render(
          request,
          "projects/usuarios.html",
          context,
      )

    elif opc == "edit":
      if pk:
        usuario = Usuario.objects.filter(email=pk).first()
        form = UsuarioForm(instance=usuario)
        context = {"altera": True, "form": form}
        return render(request, "projects/usuarios.html", context)

    elif opc == "delete":
      if pk:
        usuario = Usuario.objects.filter(email=pk).first()
        usuario.delete()

        users = Usuario.objects.all()
        filter = UsuarioFilter(request.GET, queryset=users)

        context = {"usuarios": filter, "filter": filter}
        return render(request, "projects/usuarios.html", context)

    else:
      users = Usuario.objects.all().order_by("user_id")
      filter = UsuarioFilter(request.GET, queryset=users)

      context = {"usuarios": filter, "filter": filter}
      return render(request, "projects/usuarios.html", context)

@login_required(login_url="/index")
@nivel_access_required(view_name="servicos")
def servicos(request, opc=False, pk=False):

  if request.method == "POST":
    form = ServicosForm(request.POST)
    if form.is_valid():

      codigo      = form.cleaned_data["codigo"]
      descricao   = form.cleaned_data["descricao"]
      versao      = form.cleaned_data["versao"]
      cliente     = form.cleaned_data["cliente"]
      tipo        = form.cleaned_data["tipo"]
      observacao  = form.cleaned_data["observacao"]

      if opc == "insert":

        servico = Servicos(
          codigo      = codigo,
          descricao   = descricao,
          versao      = versao,
          cliente     = cliente,
          tipo        = tipo,
          observacao  = observacao,
        )

        servico.save()

        return redirect("servicos")

      elif opc == "edit":

        servico = Servicos.objects.filter(codigo=pk).first()

        servico.descricao   = descricao
        servico.versao      = versao
        servico.cliente     = cliente
        servico.tipo        = tipo
        servico.observacao  = observacao
       
        servico.save()

        return redirect("servicos")
    else:
      erro = form.errors
      return render(
          request,
          "projects/servicos.html",
          {"altera": True, "form": form, "erro": erro},
      )
  else:

    if opc == "insert":
      form = ServicosForm()
      context = {"inclui": True, "form": form}
      return render(request, "projects/servicos.html", context)

    elif opc == "edit":
      if pk:
        servico = Servicos.objects.filter(codigo=pk).first()
        form = ServicosForm(instance=servico)
        context = {"altera": True, "form": form}
        return render(request, "projects/servicos.html", context)

    elif opc == "delete":
      if pk:
        servico = Servicos.objects.filter(codigo=pk).first()
        servico.delete()
        servicos = Servicos.objects.all()
        context = {"servicos": servicos}
        return render(request, "projects/servicos.html", context)

    else:
      servicos = Servicos.objects.all()
      context = {"servicos": servicos}
      return render(request, "projects/servicos.html", context)

@login_required(login_url="/index")
@nivel_access_required(view_name="empresas")
def empresas(request, pk=False, opc=False):
  
  if request.method == "POST":
    
    if opc == "insert":
      form = NewEmpresaForm(request.POST)
    elif opc == "edit":
      form = EmpresaForm(request.POST)

    if form.is_valid():

      codigo      = form.cleaned_data["codigo"]
      nome        = form.cleaned_data["nome"]
      cnpj        = form.cleaned_data["cnpj"]
      endereco    = form.cleaned_data["endereco"]
      cidade      = form.cleaned_data["cidade"]
      estado      = form.cleaned_data["estado"]
      telefone    = form.cleaned_data["telefone"]
      dados_bancarios = form.cleaned_data["dados_bancarios"]
      imposto     = form.cleaned_data["imposto"]

      if opc == "insert":

        empresa = Empresa(
          codigo          = codigo,
          nome            = nome,
          cnpj            = cnpj,
          endereco        = endereco,
          cidade          = cidade,
          estado          = estado,
          telefone        = telefone,
          dados_bancarios = dados_bancarios,
          imposto         = imposto,
        )

        empresa.save()

        return redirect("empresas")

      elif opc == "edit":
        
        empresa = Empresa.objects.filter(codigo=pk).first()

        empresa.nome            = nome
        empresa.cnpj            = cnpj
        empresa.endereco        = endereco
        empresa.cidade          = cidade
        empresa.estado          = estado
        empresa.telefone        = telefone
        empresa.dados_bancarios = dados_bancarios
        empresa.imposto         = imposto
        
        empresa.save()

        return redirect("empresas")
    else:
      return render(
          request,
          "projects/empresas.html",
          {"form": form, "message": form.errors, "type": "danger"},
      )
  else:

    if opc == "insert":
      form = NewEmpresaForm()
      context = {"inclui": True, "form": form}
      return render(request, "projects/empresas.html", context)

    elif opc == "edit":
      if pk:
        empresa = Empresa.objects.filter(codigo=pk).first()
        form = EmpresaForm(instance=empresa)
        context = {"altera": True, "form": form}
        return render(request, "projects/empresas.html", context)

    elif opc == "delete":
      if pk:
        empresa = Empresa.objects.filter(codigo=pk).first()
        empresa.delete()
        empresas = Empresa.objects.all()
        context = {"empresa": empresas}
        return render(request, "projects/empresas.html", context)

    else:
      empresas = Empresa.objects.all()
      context = {"empresa": empresas}
      return render(request, "projects/empresas.html", context)
           
@login_required(login_url="/index")
@nivel_access_required(view_name="niveis")
def niveis(request, pk=False, opc=False):

  if request.method == "POST":
    
    nivel_form = NivelForm(request.POST)
    if nivel_form.is_valid():

      descricao = nivel_form.cleaned_data["descricao"]
      rotina    = nivel_form.cleaned_data["rotina"]
      inclusao  = nivel_form.cleaned_data["inclusao"]
      edicao    = nivel_form.cleaned_data["edicao"]
      exclusao  = nivel_form.cleaned_data["exclusao"]
      logs      = nivel_form.cleaned_data["logs"]
      filtro    = nivel_form.cleaned_data["filtro"]
      active    = nivel_form.cleaned_data["active"]

      if opc == "insert":

        nivel = Niveis(
            descricao=descricao,
            rotina=rotina,
            inclusao=inclusao,
            edicao=edicao,
            exclusao=exclusao,
            logs=logs,
            filtro=filtro,
            active=active
        )

        nivel.save()

        return redirect("niveis")

      elif opc == "edit":

        nivel = Niveis.objects.filter(nivel_id=pk).first()

        nivel.descricao = descricao
        nivel.rotina    = rotina   
        nivel.inclusao  = inclusao 
        nivel.edicao    = edicao   
        nivel.exclusao  = exclusao 
        nivel.logs      = logs     
        nivel.filtro    = filtro   
        nivel.active    = active   

        nivel.save()

        return redirect("niveis")
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
        nivel.delete()
        niveis = Niveis.objects.all()
        context = {"niveis": niveis}
        return render(request, "projects/niveis.html", context)

    else:
      niveis = Niveis.objects.all()
      context = {"niveis": niveis}
      return render(request, "projects/niveis.html", context)

@login_required(login_url="/index")
def clientes(request, opc=False, pk=False):
  
  if request.method == "POST":
   
    form = ClienteForm(request.POST)

    if form.is_valid():

      nome                = form.cleaned_data["nome"]
      cnpj                = form.cleaned_data["cnpj"]
      ie                  = form.cleaned_data["ie"]
      endereco            = form.cleaned_data["endereco"]
      complemento         = form.cleaned_data["complemento"]
      bairro              = form.cleaned_data["bairro"]
      cidade              = form.cleaned_data["cidade"]
      estado              = form.cleaned_data["estado"]
      email               = form.cleaned_data["email"]
      email_cat           = form.cleaned_data["email_cat"]
      usa_email_cat       = form.cleaned_data["usa_email_cat"]
      telefone            = form.cleaned_data["telefone"]
      contatos            = form.cleaned_data["contatos"]
      dados_bancarios     = form.cleaned_data["dados_bancarios"]
      observacoes         = form.cleaned_data["observacoes"]
      valor_hora_atual    = form.cleaned_data["valor_hora_atual"]
      perc_desconto_atual = form.cleaned_data["perc_desconto_atual"]
      active              = form.cleaned_data["active"]

      if opc == "insert":

        cliente = Cliente(
          nome               = nome,
          cnpj               = cnpj,
          ie                 = ie,
          endereco           = endereco,
          complemento        = complemento,
          bairro             = bairro,
          cidade             = cidade,
          estado             = estado,
          email              = email,
          email_cat          = email_cat,
          usa_email_cat      = usa_email_cat,
          telefone           = telefone,
          contatos           = contatos,
          dados_bancarios    = dados_bancarios,
          observacoes        = observacoes,
          valor_hora_atual   = valor_hora_atual,
          perc_desconto_atual= perc_desconto_atual,
          active             = active,
        )

        cliente.save()

        return redirect("clientes")

      elif opc == "edit":
        
        cliente = Cliente.objects.filter(codigo=pk).first()

        cliente.nome                = nome               
        cliente.cnpj                = cnpj               
        cliente.ie                  = ie                 
        cliente.endereco            = endereco           
        cliente.complemento         = complemento        
        cliente.bairro              = bairro             
        cliente.cidade              = cidade             
        cliente.estado              = estado             
        cliente.email               = email              
        cliente.email_cat           = email_cat          
        cliente.usa_email_cat       = usa_email_cat      
        cliente.telefone            = telefone           
        cliente.contatos            = contatos           
        cliente.dados_bancarios     = dados_bancarios    
        cliente.observacoes         = observacoes        
        cliente.valor_hora_atual    = valor_hora_atual   
        cliente.perc_desconto_atual = perc_desconto_atual
        cliente.active              = active             
        
        cliente.save()

        return redirect("clientes")
    else:
      return render(
          request,
          "projects/clientes.html",
          {"form": form, "message": form.errors, "type": "danger"},
      )
  else:

    if opc == "insert":
      form = ClienteForm()
      context = {"inclui": True, "form": form}
      return render(request, "projects/clientes.html", context)

    elif opc == "edit":
      if pk:
        cliente = Cliente.objects.filter(codigo=pk).first()
        form = ClienteForm(instance=cliente)
        context = {"altera": True, "form": form}
        return render(request, "projects/clientes.html", context)

    elif opc == "delete":
      if pk:
        cliente = Cliente.objects.filter(codigo=pk).first()
        cliente.delete()
        clientes = Cliente.objects.all()
        context = {"cliente": clientes}
        return render(request, "projects/clientes.html", context)

    else:
      clientes = Cliente.objects.all()
      context = {"clientes": clientes}
      return render(request, "projects/clientes.html", context)

@login_required(login_url="/index")
def colaboradores(request, opc=False, pk=False):
  
  if request.method == "POST":
   
    form = ColaboradorForm(request.POST)

    if form.is_valid():

      codigo              = form.cleaned_data["codigo"]
      nome                = form.cleaned_data["nome"]
      cpf                 = form.cleaned_data["cpf"]
      endereco            = form.cleaned_data["endereco"]
      bairro              = form.cleaned_data["bairro"]
      cidade              = form.cleaned_data["cidade"]
      estado              = form.cleaned_data["estado"]
      email               = form.cleaned_data["email"]
      telefone            = form.cleaned_data["telefone"]
      dados_bancarios     = form.cleaned_data["dados_bancarios"]
      valor_hora          = form.cleaned_data["valor_hora"]
      valor_fixo          = form.cleaned_data["valor_fixo"]
      comissao            = form.cleaned_data["comissao"]
      funcao              = form.cleaned_data["funcao"]
      active              = form.cleaned_data["active"]
      periodo_lancamento  = form.cleaned_data["periodo_lancamento"]

      if opc == "insert":

        colaborador = Colaborador(
          codigo             = codigo,
          nome               = nome,
          cpf                = cpf,
          endereco           = endereco,
          bairro             = bairro,
          cidade             = cidade,
          estado             = estado,
          email              = email,
          telefone           = telefone,
          dados_bancarios    = dados_bancarios,
          valor_hora         = valor_hora,
          valor_fixo         = valor_fixo,
          comissao           = comissao,
          funcao             = funcao,
          active             = active,
          periodo_lancamento = periodo_lancamento,
        )

        colaborador.save()

        return redirect("colaboradores")

      elif opc == "edit":
        
        colaborador = Colaborador.objects.filter(codigo=pk).first()

        colaborador.nome               = nome
        colaborador.cpf                = cpf
        colaborador.endereco           = endereco
        colaborador.bairro             = bairro
        colaborador.cidade             = cidade
        colaborador.estado             = estado
        colaborador.email              = email
        colaborador.telefone           = telefone
        colaborador.dados_bancarios    = dados_bancarios
        colaborador.valor_hora         = valor_hora
        colaborador.valor_fixo         = valor_fixo
        colaborador.comissao           = comissao
        colaborador.funcao             = funcao
        colaborador.active             = active
        colaborador.periodo_lancamento = periodo_lancamento
        
        colaborador.save()

        return redirect("colaboradores")
    else:
      return render(
          request,
          "projects/colaboradores.html",
          {"form": form, "message": form.errors, "type": "danger"},
      )
  else:

    if opc == "insert":
      form = ColaboradorForm()
      context = {"inclui": True, "form": form}
      return render(request, "projects/colaboradores.html", context)

    elif opc == "edit":
      if pk:
        colaborador = Colaborador.objects.filter(codigo=pk).first()
        form = ColaboradorForm(instance=colaborador)
        context = {"altera": True, "form": form}
        return render(request, "projects/colaboradores.html", context)

    elif opc == "delete":
      if pk:
        colaborador = Colaborador.objects.filter(codigo=pk).first()
        colaborador.delete()
        colaboradores = Colaborador.objects.all()
        context = {"colaborador": colaboradores}
        return render(request, "projects/colaboradores.html", context)

    else:
      colaboradores = Colaborador.objects.all()
      context = {"colaboradores": colaboradores}
      return render(request, "projects/colaboradores.html", context)

@login_required(login_url="/index")
def valores(request, opc=False, pk=False):
  
  if request.method == "POST":
   
    form = ValoresForm(request.POST)

    if form.is_valid():

      codigo      = form.cleaned_data["codigo"]
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
          codigo     = codigo,
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

        valores.codigo     = codigo
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
          {"form": form, "message": form.errors, "type": "danger"},
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
def projetos(request, opc=False, pk=False):
  if request.method == "POST":
    if opc == "insert":

      form = NewProjetoForm(request.POST)
      if form.is_valid():

        projeto = Projetos(
          codigo = form.cleaned_data["codigo"],
          name = form.cleaned_data["name"],
          cliente = form.cleaned_data["cliente"],
          responsavel = form.cleaned_data["responsavel"],
          arquiteto = form.cleaned_data["arquiteto"],
          data_inicio = form.cleaned_data["data_inicio"],
          data_entrega = form.cleaned_data["data_entrega"],
          desenvolvedor = form.cleaned_data["desenvolvedor"],
          status = form.cleaned_data["status"],
          qtd_horas_apontadas = form.cleaned_data["qtd_horas_apontadas"],
          qtd_horas_projeto = form.cleaned_data["qtd_horas_projeto"],
          valor_hora = form.cleaned_data["valor_hora"],
          valor_total = form.cleaned_data["valor_total"],
        )
        projeto.save()

        return redirect("projetos")
      else:
          erro = form.errors
          return render(
              request,
              "projects/projetos.html",
              {"inclui": True, "form": form, "message": "erro", "type": "danger"},
          )
    else:
        form = ProjetoForm(request.POST)
        if form.is_valid():

          projeto = Projetos.objects.filter(codigo=pk).first()

          projeto.name          = form.cleaned_data["name"]
          projeto.cliente       = form.cleaned_data["cliente"]
          projeto.responsavel   = form.cleaned_data["responsavel"]
          projeto.arquiteto     = form.cleaned_data["arquiteto"]
          projeto.data_inicio   = form.cleaned_data["data_inicio"]
          projeto.data_entrega  = form.cleaned_data["data_entrega"]
          projeto.desenvolvedor = form.cleaned_data["desenvolvedor"]
          projeto.status        = form.cleaned_data["status"]

          projeto.save()

          return redirect("projetos")
        else:
          erro = form.errors
          print(erro)
          return render(
              request,
              "projects/projetos.html",
              {"altera": True, "form": form, "erro": erro},
          )
  else:
    if opc == "insert":
      form = NewProjetoForm()
      context = {"inclui": True, "form": form}
      return render(request, "projects/projetos.html", context)

    elif opc == "edit":
      if pk:
          projeto = Projetos.objects.filter(codigo=pk).first()
          form = ProjetoForm(instance=projeto)
          context = {"altera": True, "form": form}
          return render(request, "projects/projetos.html", context)

    elif opc == "delete":
      if pk:
          projeto = Projetos.objects.filter(codigo=pk).first()
          projeto.delete()

          projetos = Projetos.objects.all()
          filter = ProjetoFilter(request.GET, queryset=projetos)

          context = {"projetos": filter, "filter": filter}
          return render(request, "projects/projetos.html", context)

    else:
      projetos = Projetos.objects.all()

      filter = ProjetoFilter(request.GET, queryset=projetos)

      context = {"projetos": filter, "filter": filter}
      return render(request, "projects/projetos.html", context)


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
  x = Projetos.objects.all()

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
      {"descricao": "Nivel 4"},
    ]

  users = [
      {"nome": "rodrigo", "email": "rodrigo.cesar91@yahoo.com.br"},
      {"nome": "velton", "email": "velton@alphaerp.com.br"},
      {"nome": "joao", "email": "joao@alphaerp.com.br"},
      {"nome": "jose", "email": "jose@alphaerp.com.br"},
      {"nome": "antonio", "email": "antonio@alphaerp.com.br"},
      {"nome": "carlos", "email": "carlos@alphaerp.com.br"},
      {"nome": "alfredo", "email": "alfredo@alphaerp.com.br"},
    ]

  clientes = [
      {"nome": "Cliente Teste 1", "cnpj": "123456789", "telefone": "98045036","email":"emailteste.com.br", "estado":"PR"},
      {"nome": "Outro Cliente de Teste", "cnpj": "123456789", "telefone": "98045036","email":"emailteste.com.br", "estado":"PR"},
    ]

  servicos = [
      {"codigo": "SV0001", "descricao": "Serviço de Teste 1", "tipo": "Pontual"},
      {"codigo": "SV0002", "descricao": "Serviço 002", "tipo": "Sustentação"},
      {"codigo": "SERV01", "descricao": "Serviço para Testar", "tipo": "Projeto"},
    ]

  empresas = [
    {"codigo": "EMP001", "nome": "Empresa Teste", "cnpj": "07876633951", "cidade": "Curitiba", "estado": "PR", "telefone": "41998044063", "imposto": 2},
    {"codigo": "EMP002", "nome": "Empresa de Teste 2", "cnpj": "0732312456", "cidade": "Curitiba", "estado": "RJ", "telefone": "41998044063", "imposto": 10},
  ]

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
  
  for i in servicos:
    servico = Servicos(
      codigo= i['codigo'],
      descricao= i['descricao'],
      versao="001", 
      cliente=cliente,
      tipo= i['tipo'],
    )
    servico.save()
  
  for i in empresas:
    empresa = Empresa(
      codigo          = i['codigo'],
      nome            = i['nome'],
      cnpj            = i['cnpj'],
      cidade          = i['cidade'],
      estado          = i['estado'],
      telefone        = i['telefone'],
      imposto         = i['imposto'],
    )
    empresa.save()

  return redirect("home")
