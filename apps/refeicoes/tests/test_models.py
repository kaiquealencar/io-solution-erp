import pytest 
from django.core.exceptions import ValidationError
from apps.refeicoes.models import Refeicoes, RefeicaoDia


@pytest.mark.django_db
def test_criar_refeicoes():
    refeicoes = Refeicoes.objects.create(
        nome="Refeição de Teste",
        tipo="PACIENTE_ACOMPANHANTE"
    )
     
    refeicoes.full_clean()    
    refeicoes.save()

    r = Refeicoes.objects.first()

    assert r is not None

@pytest.mark.django_db
def test_criar_refeicao_dia():
    refeicoes = Refeicoes.objects.create(
        nome="Refeição de Teste",
        tipo="PACIENTE_ACOMPANHANTE"
    )
    refeicao_dia = RefeicaoDia.objects.create(
        data="2023-01-01",
        refeicao=refeicoes,
        quantidade=10
    )
    
    refeicao_dia.full_clean()    
    refeicao_dia.save()

    r = RefeicaoDia.objects.first()

    assert r is not None