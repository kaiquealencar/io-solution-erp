import pytest
from apps.empresa.models import Empresa
from apps.usuarios.models import Usuario

@pytest.fixture
def empresa_teste(db):
    return Empresa.objects.create(
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

@pytest.fixture
def usuario_gerente(db, empresa_teste):
    return Usuario.objects.create_user(
        email="gerente@iosolution.com",
        password="senha_segura_123",
        empresa=empresa_teste,
        role="gerente"
    )

@pytest.fixture
def cliente_autenticado(client, usuario_gerente):
    client.login(email="gerente@iosolution.com", password="senha_segura_123")

    return client