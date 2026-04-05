import pytest 
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.urls import reverse
from apps.usuarios.models import Usuario
from apps.empresa.models import Empresa


@pytest.mark.django_db
class TestUsuarioModel:
    
    def test_criar_usuario_gerente_sucesso(self, usuario_gerente):
        assert Usuario.objects.count() == 1
        assert usuario_gerente.email == "gerente@iosolution.com"
        assert usuario_gerente.nome == "Gerente"
        assert usuario_gerente.role == "gerente"


    def test_usuario_logado_vinculado_empresa(self, cliente_autenticado, usuario_gerente, empresa_teste):
        user_id = cliente_autenticado.session["_auth_user_id"]
        user = get_user_model().objects.get(id=user_id)

        assert user == usuario_gerente    
        assert user.empresa == empresa_teste
        assert user.empresa.razao_social == "I/O Solution LTDA"


    def teste_usuario_nao_visualiza_dados_de_outra_empresa(self, cliente_autenticado, empresa_teste):
        empresa_secundaria = Empresa.objects.create(
            razao_social="Empresa Secundaria",
            cnpj="23.499.190/0001-39",
            logradouro="Rua Nova",
            numero="56",
            bairro="Vila Maira",
            cidade="Caçapava",
            estado="SP",
            cep="122966-24",
            email="segunda@iosolution.com",
            regime_tributario = "SN",
            tipo_empresa="MATRIZ",
            matriz=None
        )

        url = reverse("empresa:listar_empresas")
        response = cliente_autenticado.get(url)
        print(f"erro na view:  {response.context['empresas']}")

        conteudo = response.content.decode()

        assert "I/O Solution LTDA" in conteudo
        assert "Empresa Secundaria" not in conteudo

    def test_erro_email_duplicado(self, usuario_gerente, empresa_teste):
        
        with pytest.raises(Exception):
            Usuario.objects.create_user(
                email="gerente@iosolution.com",
                nome="Gerente",
                password="outra_senha",
                empresa=empresa_teste
            )

    def test_usuario_comum_sem_empresa_deve_falhar(self):
        usuario = Usuario(
            email="sem_empresa@teste.com",
            nome="Usuario sem empresa",
            role="funcionario",
            password="senha_temporaria" 
        )

        with pytest.raises(ValidationError) as excinfo:
            usuario.full_clean()

        assert "empresa" in excinfo.value.message_dict        

    def test_superuser_criado_sem_empresa_com_sucesso(self):
        admin = Usuario.objects.create_superuser(
            email="admin@iosolution.com",
            nome="Admin",
            password="adminpassword"
        )

        assert admin.is_superuser
        assert admin.is_staff
        assert admin.empresa is None

    def test_email_normalizado(self, empresa_teste):
        email_maiusculo = "USER_TESTE@EXAMPLE.COM"
        
        usuario = Usuario.objects.create_user(
            email=email_maiusculo,
            nome="Teste Email",
            password="password123",
            empresa=empresa_teste
        )

        assert usuario.email == email_maiusculo.lower()


        