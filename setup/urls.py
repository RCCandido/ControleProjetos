from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from projects.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", logar_usuario, name="logar_usuario"),
    path("index", logar_usuario, name="logar_usuario"),
    path("deslogar_usuario", deslogar_usuario, name="deslogar_usuario"),
    path("empresas", empresas, name="empresas"),
    path("empresas/<opc>", empresas, name="empresas"),
    path("empresas/<opc>/<pk>", empresas, name="empresas"),
    path("usuarios", usuarios, name="usuarios"),
    path("usuarios/<opc>", usuarios, name="usuarios"),
    path("usuarios/<opc>/<pk>", usuarios, name="usuarios"),
    path("servicos", servicos, name="servicos"),
    path("servicos/<opc>", servicos, name="servicos"),
    path("servicos/<opc>/<pk>", servicos, name="servicos"),
    path("recuperar_senha", recuperar_senha, name="recuperar_senha"),
    path("redefinir_senha", redefinir_senha, name="redefinir_senha"),
    path("niveis", niveis, name="niveis"),
    path("niveis/<opc>", niveis, name="niveis"),
    path("niveis/<opc>/<pk>", niveis, name="niveis"),
    path("clientes", clientes, name="clientes"),
    path("clientes/<opc>", clientes, name="clientes"),
    path("clientes/<opc>/<pk>", clientes, name="clientes"),
    path("relatorios", relatorios, name="relatorios"),
    path("projetos", projetos, name="projetos"),
    path("projetos/<opc>", projetos, name="projetos"),
    path("projetos/<opc>/<pk>", projetos, name="projetos"),
    path("logs", logs, name="logs"),
    path(
        "retorna_total_usuarios", retorna_total_usuarios, name="retorna_total_usuarios"
    ),
    path(
        "retorna_total_projetos", retorna_total_projetos, name="retorna_total_projetos"
    ),
    path("home", home, name="home"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
