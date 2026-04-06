import pytest
from django.contrib.auth import get_user_model 
from django.urls import reverse
from apps.empresa.models import Empresa
from apps.usuarios.models import Usuario

@pytest.mark.django_db
class TestUsuario:

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

    def test_editar_usuario(self, cliente_a, usuario_a):
        novo_nome = "Nome Atualizado"

        dados_edicao = {
            "email": usuario_a.email,
            "nome": novo_nome,
            "role": "gerente",
            "is_active": True,
            "empresa": str(usuario_a.empresa.id)
        }

        url = reverse("usuarios:editar_usuario", kwargs={"id": usuario_a.id})
        response = cliente_a.post(url, data=dados_edicao)

        if response.status_code == 200:
            print(f"\nERROS DO FORMULÁRIO: {response.context['forms'].errors.as_json()}")

        assert response.status_code == 302

        usuario_a.refresh_from_db()

        assert usuario_a.nome == novo_nome
        assert usuario_a.role == "gerente"

    def test_editar_usuario_nome_vazio(self, cliente_a, usuario_a):
        url = reverse("usuarios:editar_usuario", kwargs={"id": usuario_a.id})

        dados_invalidos = {
            "email": usuario_a.email,
            "nome": "",
            "role": "funcionario",
            "is_active": True
        }

        response = cliente_a.post(url, data=dados_invalidos) 


        assert response.status_code == 200
        assert "nome" in response.context["forms"].errors
        
    def test_excluir_usuario_sucesso(self, cliente_a, usuario_a):
        usuario_a.role = 'gerente'
        usuario_a.save()
    
        usuario_alvo = Usuario.objects.create_user(
            email="alvo@test.com", 
            nome="Alvo", 
            empresa=usuario_a.empresa
        )
    
        url = reverse("usuarios:excluir_usuario", kwargs={"id": usuario_alvo.id})
        response = cliente_a.post(url)
    
        assert response.status_code == 302
        assert not Usuario.objects.filter(id=usuario_alvo.id).exists()

    def test_usuario_nao_pode_excluir_outra_empresa(self, cliente_a, usuario_a):
        empresa_b = Empresa.objects.create(
            razao_social="I/O Solution LTDA",
            nome_fantasia="I/O Solution LTDA",
            cnpj="79.800.500/0001-68",
            logradouro="avenida Brasil",
            numero="531",
            bairro="Vila Antonio Augusto",
            cidade="Caçapava",
            estado="SP",
            cep="122966-23",
            email="suporte@iosolution.com",
            regime_tributario = "SN",
            tipo_empresa="MATRIZ",
            matriz=None
        )

        usuario_b = Usuario.objects.create_user(
            email="naoremover@test.com",
            nome="Nao Remover",
            password="Rem123",
            empresa=empresa_b
        )

        url = reverse("usuarios:excluir_usuario", kwargs={"id": usuario_b.id})
        response = cliente_a.post(url)
        assert response.status_code == 302
        assert response.url == reverse("usuarios:lista_usuarios")

        assert Usuario.objects.filter(id=usuario_b.id).exists()



