import pytest
from django.contrib.auth import get_user_model
from apps.empresa.models import Empresa

User = get_user_model()

@pytest.fixture
def matriz_demo(db):
    return Empresa.objects.create(
        razao_social="I/O Solution LTDA",
        nome_fantasia="I/O Solution LTDA",
        cnpj="74.515.886/0001-42",
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
def usuario_a(db, matriz_demo):
    return User.objects.create_user(
        email='user_a@test.com',
        password='123',
        empresa=matriz_demo
    )

@pytest.fixture
def cliente_a(client, usuario_a):
    client.force_login(usuario_a)
    return client