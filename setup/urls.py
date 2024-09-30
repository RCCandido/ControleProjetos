from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from projects.views import *

urlpatterns = [
    path("", logar_usuario, name="logar_usuario"),
    path("home", home, name="home"),
    path("cargainicial", cargainicial, name="cargainicial"),
    path("index", logar_usuario, name="logar_usuario"),
    path("profile", profile, name="profile"),
    path("deslogar_usuario", deslogar_usuario, name="deslogar_usuario"),
    path("recuperar_senha", recuperar_senha, name="recuperar_senha"),
    path("redefinir_senha", redefinir_senha, name="redefinir_senha"),
    path("usuarios", usuarios, name="usuarios"),
    path("usuarios/<opc>", usuarios, name="usuarios"),
    path("usuarios/<opc>/<pk>", usuarios, name="usuarios"),
    path("empresas", empresas, name="empresas"),
    path("empresas/<opc>", empresas, name="empresas"),
    path("empresas/<opc>/<pk>", empresas, name="empresas"),
    path("servicos", servicos, name="servicos"),
    path("servicos/<opc>", servicos, name="servicos"),
    path("servicos/<opc>/<pk>", servicos, name="servicos"),
    path("grupos", grupos, name="grupos"),
    path("grupos/<opc>", grupos, name="grupos"),
    path("grupos/<opc>/<pk>", grupos, name="grupos"),
    path("clientes", clientes, name="clientes"),
    path("clientes/<opc>", clientes, name="clientes"),
    path("clientes/<opc>/<pk>", clientes, name="clientes"),
    path("colaboradores", colaboradores, name="colaboradores"),
    path("colaboradores/<opc>", colaboradores, name="colaboradores"),
    path("colaboradores/<opc>/<pk>", colaboradores, name="colaboradores"),
    path("valores", valores, name="valores"),
    path("valores/<opc>", valores, name="valores"),
    path("valores/<opc>/<pk>", valores, name="valores"),
    path("relatorios", relatorios, name="relatorios"),
    path("adicionar_item_servico", adicionar_item_servico, name="adicionar_item_servico"),
    path(
        "retorna_total_usuarios", retorna_total_usuarios, name="retorna_total_usuarios"
    ),
    path(
        "retorna_total_projetos", retorna_total_projetos, name="retorna_total_projetos"
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
