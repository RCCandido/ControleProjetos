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
    path("cadastrar_usuario", cadastrar_usuario, name="cadastrar_usuario"),
    path("empresas", empresas, name="empresas"),
    path("empresas/<pk>", empresas, name="empresas"),
    path("cadastrar_empresa", cadastrar_empresa, name="cadastrar_empresa"),
    path("usuarios", usuarios, name="usuarios"),
    path("usuarios/<opc>/<pk>", usuarios, name="usuarios"),
    path("servicos", servicos, name="servicos"),
    path("cadastrar_servico", cadastrar_servico, name="cadastrar_servico"),
    path("recuperar_senha", recuperar_senha, name="recuperar_senha"),
    path("redefinir_senha", redefinir_senha, name="redefinir_senha"),
    path("niveis", niveis, name="niveis"),
    path("niveis/<opc>", niveis, name="niveis"),
    path("niveis/<opc>/<pk>", niveis, name="niveis"),
    path("clientes", clientes, name="clientes"),
    path("relatorios", relatorios, name="relatorios"),
    path("projetos", projetos, name="projetos"),
    path(
        "retorna_total_usuarios", retorna_total_usuarios, name="retorna_total_usuarios"
    ),
    path("home", home, name="home"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
