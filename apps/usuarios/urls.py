from django.urls import path
from .views import cad_usuario, lista_usuarios, editar_usuario, excluir_usuario, validar_email

app_name = 'usuarios'

urlpatterns = [
    path('', lista_usuarios, name='lista_usuarios'),
    path('cadastrar-usuario/', cad_usuario, name='cadastrar_usuario'),
    path('editar-usuario/<int:id>/', editar_usuario, name='editar_usuario'),
    path('excluir-usuario/<int:id>/', excluir_usuario, name='excluir_usuario'),
    path('validar-email/', validar_email, name='validar_email'),
]