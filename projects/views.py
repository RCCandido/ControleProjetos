import random

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password

from .models import Usuario, Empresa, Servicos, Niveis
from .forms import UsuarioForm, NewUsuarioForm, EmpresaForm, ServicosForm, NivelForm, RedefinirSenhaForm
from .decorators import nivel_access_required

def logar_usuario(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        usuario = authenticate(request, username=email, password=password)
        if usuario is not None:
            if usuario.bloqueado == "B":
                error = "Usuário Bloqueado."
                form_login = AuthenticationForm()
                return render(request, 'projects/index.html', {"error": error, "form_login": form_login})
            else:
                login(request, usuario)
                return redirect('home')
        else:
            error = "Usuário ou Senha inválido(s)."
            form_login = AuthenticationForm()
            return render(request, 'projects/index.html', {"error": error, "form_login": form_login})
    else:
        error = ""
        form_login = AuthenticationForm()
        return render(request, 'projects/index.html', {"error": error, "form_login": form_login})


@login_required(login_url='/index')
@nivel_access_required(view_name="usuarios")
def cadastrar_usuario(request):

    if request.method == "POST":
        form = NewUsuarioForm(request.POST)
        if form.is_valid():
            
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = make_password(form.cleaned_data['password'])
            password2 = make_password(form.cleaned_data['password2'])
            bloqueado = form.cleaned_data['bloqueado']
            tipo = form.cleaned_data['tipo']
            perfil = form.cleaned_data['perfil']
            
            user = Usuario(name=name, email=email, password=password, password2=password2, bloqueado=bloqueado, tipo=tipo, perfil=perfil)
            user.save()

            return redirect('usuarios')
        else:
            return render(request, 'projects/cadastro_usuario.html', {'form': form_usuario, 'sucess': False})
    else:
        form_usuario = NewUsuarioForm()
        return render(request, 'projects/cadastro_usuario.html', {'form': form_usuario, 'sucess': True})
    
@login_required(login_url='/index')
def redefinir_senha(request):
    form = RedefinirSenhaForm(instance=request.user)

    if request.method == 'POST':
        novasenha = request.POST['password']
        novasenha2 = request.POST['password2']
        
        if novasenha != novasenha2:
            erro = "As senhas não conferem."
            return render(request, 'projects/redefinir_senha.html', {'form': form, 'erro': erro})
        else:
            user = Usuario.objects.filter(email=request.user.email).first()
            if user:
                user.set_password(novasenha)
                message = "Senha alterada com sucesso!"
                return render(request, 'projects/logoff.html', {'message': message, 'type': "success"})

    return render(request, 'projects/redefinir_senha.html', {'form': form, 'erro': ""})

def recuperar_senha(request):
    sucess = False
    invalidEmail = False
    if request.method == "POST":

        destinatario = request.POST['email']
        if destinatario:

            # verifica se o destinatario tem o email cadastrado
            user = Usuario.objects.filter(email=destinatario).first()
            if user:
                
                # cria nova senha aleatoria
                nova_senha = SenhaAleatoria()
                
                senha_criptografada = make_password(password=nova_senha, salt=None, hasher='pbkdf2_sha256')

                user.password = senha_criptografada
                user.save()

                mensagem = "Olá "+ user.name +" Sua nova senha é: "+ nova_senha

                # envia email de recuperação de senha
                send_mail(
                    "Recuperação de Senha",
                    mensagem,
                    "rodrigo.candido@alphaerp.com.br",
                    [destinatario],
                    fail_silently=False,
                )
                sucess = True
                invalidEmail = False
                return render(request, 'projects/recuperar_senha.html', {'sucess': sucess, 'invalidEmail': invalidEmail})
            else:
                sucess = False
                invalidEmail = True
                return render(request, 'projects/recuperar_senha.html', {'sucess': sucess, 'invalidEmail': invalidEmail})

        else:
            sucess = False
            invalidEmail = True
            return render(request, 'projects/recuperar_senha.html', {'sucess': sucess, 'invalidEmail': invalidEmail})

    else:
        return render(request, 'projects/recuperar_senha.html', {'sucess': sucess, 'invalidEmail': invalidEmail})


@login_required(login_url='/index')
def home(request):
  return render(request, "projects/home.html", { 'user': request.user, 'qtdUsuarios': 10, 'qtdServicos': 1 })

@login_required(login_url='/index')
@nivel_access_required(view_name="niveis")
def niveis(request, pk=False):
    if request.method == "POST":
        nivel_form = NivelForm(request.POST)
        if nivel_form.is_valid():
            nivel_form.save()
            return redirect('niveis')
    else:
        if pk:
            if pk == "incluir":
                nivel_form = NivelForm()
                return render(request, 'projects/niveis.html', {'inclui': True, 'form': nivel_form })
            
            elif isInt(pk):
                nivel = Niveis.objects.filter(nivel_id=pk)
                return render(request, 'projects/niveis.html', {'altera': True, 'form': nivel })
        else:
            niveis = Niveis.objects.all()
            return render(request, 'projects/niveis.html', {'niveis': niveis })

@login_required(login_url='/index')
def deslogar_usuario(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/index')
def empresas(request, pk=False):
    if pk:
        empresa = Empresa.objects.filter(codigo=pk)
        return render(request, 'projects/editar_empresa.html', {'empresa': empresa })
    else:
        empresas = Empresa.objects.all()
        return render(request, 'projects/empresas.html', {'empresa': empresas })

@login_required(login_url='/index')
def cadastrar_empresa(request):
    if request.method == "POST":
        form_empresa = EmpresaForm(request.POST)
        if form_empresa.is_valid():
            form_empresa.save()
            return redirect('empresas')
        else:
            form_empresa = EmpresaForm()
            return render(request, 'projects/cadastro_empresa.html', {'form': form_empresa})
    else:
        form_empresa = EmpresaForm()
        return render(request, 'projects/cadastro_empresa.html', {'form': form_empresa})


@login_required(login_url='/index')
@nivel_access_required(view_name="usuarios")
def usuarios(request, opc=False, pk=False):

    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            
            usuario = Usuario.objects.filter(email=pk).first()

            usuario.name = form.cleaned_data['name']
            usuario.bloqueado = form.cleaned_data['bloqueado']
            usuario.tipo = form.cleaned_data['tipo']
            usuario.perfil = form.cleaned_data['perfil']
            
            usuario.save()

            return redirect('usuarios')
        else:
            erro = form.errors
            return render(request, 'projects/usuarios.html', {'altera': True, 'form': form, 'erro': erro })

    else:
        if opc == "editar":
            if pk:
                usuario = Usuario.objects.filter(email=pk).first()
                form = UsuarioForm(instance=usuario)
                return render(request, 'projects/usuarios.html', {'altera': True, 'form': form })
            
        elif opc == "delete":
            if pk:
                usuario = Usuario.objects.filter(email=pk).first()
                usuario.delete()
                users = Usuario.objects.all()
                return render(request, 'projects/usuarios.html', {'usuarios': users })

        else:
            users = Usuario.objects.all()
            return render(request, 'projects/usuarios.html', {'usuarios': users })



@login_required(login_url='/index')
@nivel_access_required(view_name="servicos")
def servicos(request):
    servicos = Servicos.objects.all()
    return render(request, 'projects/servicos.html', {'servicos': servicos })

@login_required(login_url='/index')
@nivel_access_required(view_name="servicos")
def cadastrar_servico(request):
    if request.method == "POST":
        form_servico = ServicosForm(request.POST)
        if form_servico.is_valid():
            form_servico.save()
            return redirect('servicos')
        else:
            form_servico = ServicosForm()
            return render(request, 'projects/cadastro_servicos.html', {'form': form_servico})
    else:
        form_servico = ServicosForm()
        return render(request, 'projects/cadastro_servicos.html', {'form': form_servico})





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
