import random

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password

from .models import Usuario, Empresa, Servicos, Niveis
from .forms import UsuarioForm, EmpresaForm, ServicosForm, NivelForm

def logar_usuario(request):
    error = ""
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        usuario = authenticate(request, username=email, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('home')
        else:
            error = "Erro"
            form_login = AuthenticationForm()
    else:
        error = ""
        form_login = AuthenticationForm()

    return render(request, 'projects/index.html', {"error": error, "form_login": form_login})

 

# def cadastrar_usuario(request):
#     if request.method == "POST":
#         form_usuario = UserCreationForm(request.POST)
#         if form_usuario.is_valid():
#             form_usuario.save()
#             return redirect('index')
#         else:
#             invalidPassword = True
#             return render(request, 'projects/cadastro_usuario.html', {'form_usuario': form_usuario, 'invalidPassword': invalidPassword})
#     else:
#         invalidPassword = False
#         form_usuario = UserCreationForm()
#         return render(request, 'projects/cadastro_usuario.html', {'form_usuario': form_usuario, 'invalidPassword': invalidPassword})

def cadastrar_usuario(request):
    invalidPassword = False
    sucess = False
    if request.method == "POST":
        form_usuario = UsuarioForm(request.POST)
        if form_usuario.is_valid():
            
            nova_senha = request.POST['password']
            form_usuario.password = make_password(password=nova_senha, salt=None, hasher='pbkdf2_sha256')
            
            nova_senha = request.POST['password2']
            form_usuario.password2 = make_password(password=nova_senha, salt=None, hasher='pbkdf2_sha256')
            
            form_usuario.save()
            
            return render(request, 'projects/cadastro_usuario.html', {'form': form_usuario, 'invalidPassword': invalidPassword, 'sucess': sucess})
        else:
            invalidPassword = True
            return render(request, 'projects/cadastro_usuario.html', {'form': form_usuario, 'invalidPassword': invalidPassword, 'sucess': sucess})
    else:
        form_usuario = UsuarioForm()
        return render(request, 'projects/cadastro_usuario.html', {'form': form_usuario, 'invalidPassword': invalidPassword, 'sucess': sucess})
    
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
def usuarios(request, opc=False, pk=False):
    if request.method == "POST":
        userform = UsuarioForm(request.POST)
        if userform.is_valid():
            userform.save()
            return redirect('usuarios')
        else:
            return redirect('usuarios')

    else:
        if opc == "alterar":
            if pk:
                usuario = Usuario.objects.filter(email=pk).first()
                userform = UsuarioForm(instance=usuario)
                return render(request, 'projects/usuarios.html', {'altera': True, 'form': userform })
        elif opc == "delete":
            if pk:
                usuario = Usuario.objects.filter(email=pk).first()
                usuario.delete()
                User = get_user_model()
                users = User.objects.all()
                return render(request, 'projects/usuarios.html', {'usuarios': users })

        else:
            User = get_user_model()
            users = User.objects.all()
            return render(request, 'projects/usuarios.html', {'usuarios': users })

@login_required(login_url='/index')
def servicos(request):
    servicos = Servicos.objects.all()
    return render(request, 'projects/servicos.html', {'servicos': servicos })

@login_required(login_url='/index')
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