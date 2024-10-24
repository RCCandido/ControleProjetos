from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import ItemGrupo

def empresas_test_function(user):
  
  # se usuario ativo e possui um perfil
  if user.active and user.perfil_id:
    
    if temAcesso(user.perfil_id, "1"):
      return True
  
  return False

def grupos_test_function(user):
  
  # se usuario ativo e possui um perfil
  if user.active and user.perfil_id:
    
    if temAcesso(user.perfil_id, "2"):
      return True
  
  return False

def usuarios_test_function(user):
  
  # se usuario ativo e possui um perfil
  if user.active and user.perfil_id:
    
    if temAcesso(user.perfil_id, "3"):
      return True
  
  return False

def clientes_test_function(user):
  
  # se usuario ativo e possui um perfil
  if user.active and user.perfil_id:
    
    if temAcesso(user.perfil_id, "4"):
      return True
  
  return False

def servicos_test_function(user):
  
  # se usuario ativo e possui um perfil
  if user.active and user.perfil_id:
    
    if temAcesso(user.perfil_id, "5"):
      return True
  
  return False

def colaboradores_test_function(user):
  
  # se usuario ativo e possui um perfil
  if user.active and user.perfil_id:
    
    if temAcesso(user.perfil_id, "6"):
      return True
  
  return False



def nivel_access_required(view_name):
  match view_name:

    case "servicos":
      def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
          if request.user.resetpsw:
            return redirect("redefinir_senha")

          if not servicos_test_function(request.user):
            context = {
                "type": "danger",
                "title": "Serviços",
                "message": "Você não tem permissão de acesso à esta página.",
            }
            return render(request, "projects/notpermited.html", context)

          return view(request, *args, **kwargs)

        return _wrapped_view

      return decorator

    case "usuarios":
      def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
          if request.user.resetpsw:
            return redirect("redefinir_senha")

          if not usuarios_test_function(request.user):
            context = {
                "type": "danger",
                "title": "Usuários",
                "message": "Você não tem permissão de acesso à esta página.",
            }
            return render(request, "projects/notpermited.html", context)

          return view(request, *args, **kwargs)
        return _wrapped_view
      return decorator

    case "grupos":
      def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
          if request.user.resetpsw:
            return redirect("redefinir_senha")

          if not grupos_test_function(request.user):
            context = {
                "type": "danger",
                "title": "Grupos de Acesso",
                "message": "Você não tem permissão de acesso à esta página.",
            }
            return render(request, "projects/notpermited.html", context)

          return view(request, *args, **kwargs)
        return _wrapped_view
      return decorator

    case "empresas":
      def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
          if request.user.resetpsw:
            return redirect("redefinir_senha")

          if not empresas_test_function(request.user):
            context = {
                "type": "danger",
                "title": "Empresas",
                "message": "Você não tem permissão de acesso à esta página.",
            }
            return render(request, "projects/notpermited.html", context)
        
          return view(request, *args, **kwargs)
        return _wrapped_view
      return decorator
    
    case "clientes":
      def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
          if request.user.resetpsw:
            return redirect("redefinir_senha")

          if not clientes_test_function(request.user):
            context = {
                "type": "danger",
                "title": "Clientes",
                "message": "Você não tem permissão de acesso à esta página.",
            }
            return render(request, "projects/notpermited.html", context)
        
          return view(request, *args, **kwargs)
        return _wrapped_view
      return decorator
    
    case "colaboradores":
      def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
          if request.user.resetpsw:
            return redirect("redefinir_senha")

          if not colaboradores_test_function(request.user):
            context = {
                "type": "danger",
                "title": "Colaboradores",
                "message": "Você não tem permissão de acesso à esta página.",
            }
            return render(request, "projects/notpermited.html", context)
        
          return view(request, *args, **kwargs)
        return _wrapped_view
      return decorator


def temAcesso(perfil, rotina):
  ##("1", "Empresas")
  ##("2", "Grupos")
  ##("3", "Usuários")
  ##("4", "Clientes")
  ##("5", "Serviços")
  ##("6", "Colaboradores")
  return ItemGrupo.objects.filter(grupo_id=perfil, rotina=rotina).first() 