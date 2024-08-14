
from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse
 
 
def servicos_test_function(user):
    if not user.bloqueado and user.perfil == "N1":
        return True
    return False
 
 
def usuarios_test_function(user):
    if user.perfil == "N1":
        return True
    return False
 
 
def niveis_test_function(user):
    if user.perfil == "N1":
        return True
    return False

def empresas_test_function(user):
    if user.perfil == "N1":
        return True
    return False
 
 
def nivel_access_required(view_name):
    match view_name:
        case "servicos":
          def decorator(view):
              @wraps(view)
              def _wrapped_view(request, *args, **kwargs):
                  if not servicos_test_function(request.user):
                      return HttpResponse("Você não tem permissão \
                              de acesso à esta pagina!")
                  return view(request, *args, **kwargs)
              return _wrapped_view
          return decorator
        
        case "usuarios":
          def decorator(view):
              @wraps(view)
              def _wrapped_view(request, *args, **kwargs):
                  if not usuarios_test_function(request.user):
                      return HttpResponse("Você não tem permissão \
                              de acesso à esta pagina!")
                  return view(request, *args, **kwargs)
              return _wrapped_view
          return decorator
        
        case "niveis":
          def decorator(view):
              @wraps(view)
              def _wrapped_view(request, *args, **kwargs):
                  if not niveis_test_function(request.user):
                      return HttpResponse("Você não tem permissão \
                              de acesso à esta pagina!")
                  return view(request, *args, **kwargs)
              return _wrapped_view
          return decorator
       
        case "empresas":
          def decorator(view):
              @wraps(view)
              def _wrapped_view(request, *args, **kwargs):
                  if not empresas_test_function(request.user):
                      return HttpResponse("Você não tem permissão \
                              de acesso à esta pagina!")
                  return view(request, *args, **kwargs)
              return _wrapped_view
          return decorator
