from django.urls import path
from django.contrib.auth import views as auth_views
from .views import cad_usuario, lista_usuarios, editar_usuario, excluir_usuario, validar_email, CustomLoginView


app_name = 'usuarios'

urlpatterns = [
    path('', lista_usuarios, name='lista_usuarios'),
    path('cadastrar-usuario/', cad_usuario, name='cadastrar_usuario'),
    path('editar-usuario/<int:id>/', editar_usuario, name='editar_usuario'),
    path('excluir-usuario/<int:id>/', excluir_usuario, name='excluir_usuario'),
    path('validar-email/', validar_email, name='validar_email'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='usuarios:login'), name='logout'),
]