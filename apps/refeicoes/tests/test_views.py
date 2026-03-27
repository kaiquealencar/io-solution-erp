import pytest
from django.urls import reverse 
from apps.refeicoes.models import RefeicaoDia, Refeicoes

@pytest.mark.django_db
def test_listar_refeicoes(client):  
    Refeicoes.objects.create(nome="Refeição 1", tipo="PACIENTE_ACOMPANHANTE")
    Refeicoes.objects.create(nome="Refeição 2", tipo="PACIENTE_ACOMPANHANTE")

    response = client.get(reverse("refeicoes:listar_refeicoes"))
    assert response.status_code == 200
    assert len(response.context["refeicoes"]) == 2

@pytest.mark.django_db
def test_cadastrar_refeicao(client):
    data = {
        "nome": "Refeição Teste",
        "tipo": "PACIENTE_ACOMPANHANTE"
    }
    response = client.post(reverse("refeicoes:cadastrar_refeicao"), data)
    assert response.status_code == 302
    assert Refeicoes.objects.filter(nome="Refeição Teste").exists()

@pytest.mark.django_db
def test_editar_refeicao(client):   
    refeicao = Refeicoes.objects.create(nome="Refeição Antiga", tipo="PACIENTE_ACOMPANHANTE")
    data = {
        "nome": "Refeição Editada",
        "tipo": "PACIENTE_ACOMPANHANTE"
    }
    response = client.post(reverse("refeicoes:editar_refeicao", args=[refeicao.id]), data)
    assert response.status_code == 302
    refeicao.refresh_from_db()
    assert refeicao.nome == "Refeição Editada"

@pytest.mark.django_db
def test_excluir_refeicao(client):
    refeicao = Refeicoes.objects.create(nome="Refeição a Excluir", tipo="PACIENTE_ACOMPANHANTE")
    response = client.post(reverse("refeicoes:excluir_refeicao", args=[refeicao.id]))
    assert response.status_code == 302
    assert not Refeicoes.objects.filter(id=refeicao.id).exists()

@pytest.mark.django_db
def test_listar_refeicoes_dia(client):
    Refeicao = Refeicoes.objects.create(nome="Refeição Teste", tipo="PACIENTE_ACOMPANHANTE")
    RefeicaoDia.objects.create(refeicao=Refeicao, data="2024-06-01")
    RefeicaoDia.objects.create(refeicao=Refeicao, data="2024-06-02")

    response = client.get(reverse("refeicoes:listar_refeicoes_dia"))
    assert response.status_code == 200
    assert len(response.context["refeicoes_dia"]) == 2
    
@pytest.mark.django_db
def test_cadastrar_refeicao_dia(client):
    refeicao = Refeicoes.objects.create(nome="Almoço", tipo="FUNCIONARIOS")
    
    data = {
        "data": "2026-03-27",      # Data no formato ISO
        "refeicao": str(refeicao.id), # O ID deve ser passado como string
        "quantidade": "10"         # Verifique se este campo aceita números no Model
    }
    
    response = client.post(reverse("refeicoes:cadastrar_refeicao_dia"), data)
    
    # Se falhar, o print abaixo mostrará a mensagem de erro no console (use pytest -s)
    if response.status_code != 302:
        print(response.content.decode()) 

    assert response.status_code == 302
    assert RefeicaoDia.objects.count() == 1

@pytest.mark.django_db
def test_editar_refeicao_dia(client):
    refeicao = Refeicoes.objects.create(nome="Refeição Teste", tipo="PACIENTE_ACOMPANHANTE")
    refeicao_dia = RefeicaoDia.objects.create(refeicao=refeicao, data="2024-06-01", quantidade=1)
    
    data = {
        "refeicao": refeicao.id,
        "data": "2024-06-02",
        "quantidade": "2" # ADICIONE ISSO
    }
    response = client.post(reverse("refeicoes:editar_refeicao_dia", args=[refeicao_dia.id]), data)
    assert response.status_code == 302

@pytest.mark.django_db
def test_excluir_refeicao_dia(client):
    Refeicao = Refeicoes.objects.create(nome="Refeição Teste", tipo="PACIENTE_ACOMPANHANTE")
    refeicao_dia = RefeicaoDia.objects.create(refeicao=Refeicao, data="2024-06-01")
    response = client.post(reverse("refeicoes:excluir_refeicao_dia", args=[refeicao_dia.id]))
    assert response.status_code == 302
    assert not RefeicaoDia.objects.filter(id=refeicao_dia.id).exists()

@pytest.mark.django_db
def test_listar_refeicoes_dia(client):
    refeicao = Refeicoes.objects.create(nome="Refeição Teste", tipo="PACIENTE_ACOMPANHANTE")
    RefeicaoDia.objects.create(refeicao=refeicao, data="2024-06-01", quantidade=1)
    RefeicaoDia.objects.create(refeicao=refeicao, data="2024-06-02", quantidade=1)

    # Forçar o mês correto na URL para o filtro encontrar os dados
    response = client.get(reverse("refeicoes:listar_refeicoes_dia"), {"mes": "2024-06"})
    
    assert response.status_code == 200
    assert len(response.context["refeicoes_dia"]) == 2