import pytest
from django.contrib.auth import get_user_model 
from django.urls import reverse
from apps.empresa.models import Empresa

User = get_user_model()

@pytest.mark.django_db
class TestEmpresaListView:

    def test_acesso_negado_anonimo(self, client):
        url = reverse("empresa:listar_empresas")
        response = client.get(url)

        assert response.status_code == 302
        assert "/login/" in response.url

    def test_usuario_logado_ve_apenas_uma_empresa(self, cliente_a, matriz_demo):
        Empresa.objects.create(
            razao_social="Outro Grupo LTDA",
            cnpj="60.399.845/0001-23",
            logradouro="avenida Brasil",
            numero="531",
            bairro="Vila Antonio Augusto",
            cidade="Caçapava",
            estado="SP",
            cep="122966-23",
            email="suporte@iosolution.com",
            regime_tributario = "SN",
        )

        url = reverse("empresa:listar_empresas")
        response = cliente_a.get(url)
        
        content = response.content.decode()
        assert response.status_code == 200
        assert matriz_demo.nome_fantasia in content
        assert "Outro Grupo LTDA" not in content


@pytest.mark.django_db
class TesteEmpresaDetailView():
    
    def test_nao_visualiza_empresa_de_outro_grupo(self, cliente_a):
        outra_empresa =   Empresa.objects.create(
            razao_social="Invasao",
            cnpj="10.199.061/0001-83",
            logradouro="avenida Brasil",
            numero="531",
            bairro="Vila Antonio Augusto",
            cidade="Caçapava",
            estado="SP",
            cep="122966-23",
            email="suporte@iosolution.com",
            regime_tributario = "SN",
        )

        url = reverse("empresa:editar_empresa", kwargs={"id": outra_empresa.id})
        response = cliente_a.get(url)

        assert response.status_code == 404
