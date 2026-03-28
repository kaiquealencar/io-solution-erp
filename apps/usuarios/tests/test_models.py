import pytest 
from django.core.exceptions import ValidationError
from apps.usuarios.models import Usuario
from apps.empresa.models import Empresa


@pytest.mark.django_db
def test_criar_usuario():    
    empresa = Empresa.objects.create(razao_social="Empresa Teste")

    usuario = Usuario.objects.create_user(
        email="example@example.com.br",
        nome="fulano",
        password="senha123",
        empresa = empresa,
        role="admin"
    )
     
    usuario.full_clean()    
    usuario.save()

    u = Usuario.objects.first()

    assert u.email == "example@example.com.br"
    assert u.nome == "fulano"
    assert u.role == "admin"
    assert u.check_password("senha123") 
    
@pytest.mark.django_db
def test_editar_usuario():
    empresa = Empresa.objects.create(razao_social="Empresa Teste")

    usuario = Usuario.objects.create_user(
        email="example@example",
        nome="fulano",
        password="senha123",
        empresa=empresa,
        role="admin"
    )

    usuario.email = "email_edit@example.com"
    usuario.full_clean()
    usuario.save()

    usuario_atualizado = Usuario.objects.get(id=usuario.id)

    assert usuario_atualizado.email == "email_edit@example.com"
    assert usuario_atualizado.nome == "fulano"
    assert usuario_atualizado.role == "admin"

@pytest.mark.django_db
def test_excluir_usuario():
    usuario = Usuario.objects.create_user(
        email="example@example",
        nome="fulano",
        password="senha123",
        role="admin"
    )

    usuario.delete()

    assert Usuario.objects.count() == 0 