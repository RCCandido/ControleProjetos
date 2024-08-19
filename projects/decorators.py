from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse

def servicos_test_function(user):
    return True
    if user.active and user.perfil == "N1":
        return True
    return False

def usuarios_test_function(user):
    return True
    if user.perfil == "":
        return True
    return False

def niveis_test_function(user):
    return True
    if user.perfil == "N1":
        return True
    return False

def empresas_test_function(user):
    return True
    if user.perfil == "N1":
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

        case "niveis":
            def decorator(view):
                @wraps(view)
                def _wrapped_view(request, *args, **kwargs):
                    if request.user.resetpsw:
                        return redirect("redefinir_senha")

                    if not niveis_test_function(request.user):
                        context = {
                            "type": "danger",
                            "title": "Níveis",
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
