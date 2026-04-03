import pytest 
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from apps.usuarios.models import Usuario
from apps.empresa.models import Empresa


@pytest.mark.django_db
class TestUsuarioModel:
    
    def test_criar_usuario_gerente_sucesso(self, usuario_gerente):
        assert Usuario.objects.count() == 1
        assert usuario_gerente.email == "gerente@iosolution.com"
        assert usuario_gerente.role == "gerente"


    def test_usuario_logado_vinculado_empresa(self, cliente_autenticado, usuario_gerente, empresa_teste):
        user_id = cliente_autenticado.session["_auth_user_id"]
        user = get_user_model().objects.get(id=user_id)

        assert user == usuario_gerente    
        assert user.empresa == empresa_teste
        assert user.empresa.razao_social == "I/O Solution LTDA"

        