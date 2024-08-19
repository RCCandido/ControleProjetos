import random

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse

from .models import Usuario, Empresa, Servicos, Niveis
from .forms import (
    UsuarioForm,
    NewUsuarioForm,
    EmpresaForm,
    ServicosForm,
    NivelForm,
    RedefinirSenhaForm,
)
from .decorators import nivel_access_required
from .filters import UsuarioFilter


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
                initial_pass = "123456"

                name = "novousuario"
                email = destinatario
                password = make_password(initial_pass)
                password2 = make_password(initial_pass)
                active = True
                tipo = "1"

                user = Usuario(
                    name=name,
                    email=email,
                    password=password,
                    password2=password2,
                    active=active,
                    tipo=tipo,
                )
                user.save()

                mensagem = "Criado primeiro acesso:\n"
                mensagem += "Usuario: " + email + "\n"
                mensagem += "Senha: " + initial_pass

                send_mail(
                    "Primeiro Acesso",
                    mensagem,
                    "rodrigo.candido@alphaerp.com.br",
                    [destinatario],
                    fail_silently=False,
                )
                sucess = True
                message = "Email enviado com o primeiro acesso."
                context = {"sucess": sucess, "message": message}
                return render(request,"projects/recuperar_senha.html",
                    context,
                )
            
                #sucess = False
                #message = "E-mail inválido, não consta na base de dados."
                #return render(
                #    request,
                #    "projects/recuperar_senha.html",
                #    {"sucess": sucess, "message": message},
                #)

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
    usuarios = Usuario.objects.all().count()
    servicos = Servicos.objects.all().count()
    niveis = Niveis.objects.all().count()

    context = {"qtdUsuarios": usuarios, "qtdServicos": servicos, "qtdNiveis": niveis}
    return render(request, "projects/home.html", context)


@login_required(login_url="/index")
@nivel_access_required(view_name="usuarios")
def usuarios(request, opc=False, pk=False):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():

            usuario = Usuario.objects.filter(email=pk).first()

            usuario.firstname = form.cleaned_data["firstname"]
            usuario.name = form.cleaned_data["name"]
            usuario.active = form.cleaned_data["active"]
            usuario.tipo = form.cleaned_data["tipo"]
            usuario.perfil = form.cleaned_data["perfil"]
            usuario.usefilter = form.cleaned_data["usefilter"]

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
        if opc == "edit":
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
            users = Usuario.objects.all()

            filter = UsuarioFilter(request.GET, queryset=users)

            context = {"usuarios": filter, "filter": filter}
            return render(request, "projects/usuarios.html", context)


@login_required(login_url="/index")
@nivel_access_required(view_name="servicos")
def servicos(request):
    servicos = Servicos.objects.all()
    return render(request, "projects/servicos.html", {"servicos": servicos})


@login_required(login_url="/index")
@nivel_access_required(view_name="empresas")
def empresas(request, pk=False):
    if pk:
        empresa = Empresa.objects.filter(codigo=pk)
        return render(request, "projects/editar_empresa.html", {"empresa": empresa})
    else:
        empresas = Empresa.objects.all()
        return render(request, "projects/empresas.html", {"empresa": empresas})


@login_required(login_url="/index")
@nivel_access_required(view_name="niveis")
def niveis(request, pk=False, opc=False):
    if request.method == "POST":
        nivel_form = NivelForm(request.POST)
        if nivel_form.is_valid():

            descricao = nivel_form.cleaned_data["descricao"]
            rotina = nivel_form.cleaned_data["rotina"]
            inclusao = nivel_form.cleaned_data["inclusao"]
            edicao = nivel_form.cleaned_data["edicao"]
            exclusao = nivel_form.cleaned_data["exclusao"]
            logs = nivel_form.cleaned_data["logs"]
            filtro = nivel_form.cleaned_data["filtro"]
            active = nivel_form.cleaned_data["active"]

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
            return render(request, "projects/niveis.html", {"niveis": niveis})

@login_required(login_url="/index")
def clientes(request):
    context = {
        "type": "primary",
        "title": "Clientes",
        "message": "Página em construção.",
    }
    return render(request, "projects/em_construcao.html", context)

@login_required(login_url="/index")
def relatorios(request):
    context = {
        "type": "primary",
        "title": "Relatórios",
        "message": "Página em construção.",
    }
    return render(request, "projects/em_construcao.html", context)

@login_required(login_url="/index")
def projetos(request):
    context = {
        "type": "primary",
        "title": "Projetos",
        "message": "Página em construção.",
    }
    return render(request, "projects/em_construcao.html", context)

## CADASTROS ##
@login_required(login_url="/index")
@nivel_access_required(view_name="usuarios")
def cadastrar_usuario(request):
    message = ""
    if request.method == "POST":
        form = NewUsuarioForm(request.POST)
        if form.is_valid():

            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            password = make_password(form.cleaned_data["password"])
            password2 = make_password(form.cleaned_data["password2"])
            active = form.cleaned_data["active"]
            tipo = form.cleaned_data["tipo"]
            perfil = form.cleaned_data["perfil"]

            user = Usuario(
                name=name,
                email=email,
                password=password,
                password2=password2,
                active=active,
                tipo=tipo,
                perfil=perfil,
            )
            user.save()

            message = "Usuário criado com Sucesso!"
            return redirect("usuarios")
        else:
            message = "As senhas não conferem."
            return render(
                request,
                "projects/cadastro_usuario.html",
                {"form": form_usuario, "message": message, "type": "danger"},
            )
    else:
        form_usuario = NewUsuarioForm()
        return render(
            request,
            "projects/cadastro_usuario.html",
            {"form": form_usuario, "message": message, "type": "success"},
        )


@login_required(login_url="/index")
@nivel_access_required(view_name="servicos")
def cadastrar_servico(request):
    if request.method == "POST":
        form_servico = ServicosForm(request.POST)
        if form_servico.is_valid():
            form_servico.save()
            return redirect("servicos")
        else:
            form_servico = ServicosForm()
            return render(
                request, "projects/cadastro_servicos.html", {"form": form_servico}
            )
    else:
        form_servico = ServicosForm()
        return render(
            request, "projects/cadastro_servicos.html", {"form": form_servico}
        )


@login_required(login_url="/index")
@nivel_access_required(view_name="empresas")
def cadastrar_empresa(request):
    if request.method == "POST":
        form_empresa = EmpresaForm(request.POST)
        if form_empresa.is_valid():
            form_empresa.save()
            return redirect("empresas")
        else:
            form_empresa = EmpresaForm()
            return render(
                request, "projects/cadastro_empresa.html", {"form": form_empresa}
            )
    else:
        form_empresa = EmpresaForm()
        return render(request, "projects/cadastro_empresa.html", {"form": form_empresa})


############ DASHBOARD ############
def retorna_total_usuarios(request):
    # total = Usuario.objects.all().aggregate(Sum('total'))['total__sum']
    total = Usuario.objects.all().count()
    return JsonResponse({'total_usuarios': total})


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
