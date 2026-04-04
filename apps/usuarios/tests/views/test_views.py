import pytest
from django.contrib.auth import get_user_model 
from django.urls import reverse
from apps.empresa.models import Empresa
from apps.usuarios.models import Usuario

@pytest.mark.django_db
class TestUsuarioList:

    def test_acesso_negado_anonimo(self, client):
        url = reverse("usuarios:lista_usuarios")
        response = client.get(url)

        assert response.status_code == 302
        assert "/login" in response.url


    def test_usuario_logado_ve_apenas_uma_empresa(self, cliente_a, matriz_demo):     
        url = reverse("usuarios:lista_usuarios")
        response = cliente_a.get(url)       
        
        assert response.status_code == 200
        assert matriz_demo.nome_fantasia in response.content.decode()

    def test_listar_usuarios_da_empresa_ativa(self, cliente_a, usuario_a): 
        Usuario.objects.create_user(
            email="funcionario_novo@teste.com",
            nome="Novo Funcionario",
            password="123",
            role="funcionario",
            empresa=usuario_a.empresa 
        )

        url = reverse("usuarios:lista_usuarios")
        response = cliente_a.get(url)

        assert response.status_code == 200
        assert len(response.context["usuarios"]) >= 2
        assert "funcionario_novo@teste.com" in response.content.decode()



    def test_cadastro_usuario_sucesso(self, cliente_a, usuario_a):
        dados = {
            "email": "novo@iosolution.com",
            "nome": "novo funcionario",
            "password": "novo123",
            "role": "funcionario",
            "is_active": True
        }

        url = reverse("usuarios:cadastrar_usuario")
        response = cliente_a.post(url, data=dados)

        assert response.status_code == 302
        
        novo_usuario = Usuario.objects.get(email="novo@iosolution.com")

        assert novo_usuario.empresa == usuario_a.empresa
        assert novo_usuario.nome == "novo funcionario"






