from urllib import response

import pytest
from django.urls import reverse 
from apps.empresa.models import Empresa


@pytest.mark.django_db
def test_listar_empresas(client):   
    Empresa.objects.create(
        razao_social="Empresa Teste LTDA",
        nome_fantasia="Empresa Teste",
        cnpj="52.038.391/0001-37",
        inscricao_estadual="123456789",
        inscricao_municipal="987654321",
        logradouro="Rua Teste",
        numero="123",
        complemento="Sala 1",
        bairro="Centro",
        cidade="Cidade Teste",
        estado="ST",
        cep="12345-678",
        pais="Brasil",
        logo="logo.png",
        regime_tributario="SN",
        cnae_principal="6201-5/01",
        moeda_padrao="BRL",
        certificado_digital="certificado.pfx",
        senha_certificado="senha123",
        telefone="(11) 1234-5678",
        email="example@example.com.br",
        tipo_empresa='MATRIZ',
    )
    response = client.get(reverse('empresa:listar_empresas'))
    assert response.status_code == 200
    assert len(response.context['empresas']) == 1

@pytest.mark.django_db
def test_cadastrar_empresa(client):
    data = {
        "razao_social": "Empresa Teste LTDA",
        "nome_fantasia": "Empresa Teste",
        "cnpj": "52.038.391/0001-37",
        "inscricao_estadual": "123456789",
        "inscricao_municipal": "987654321",
        "logradouro": "Rua Teste",
        "numero": "123",
        "complemento": "Sala 1",
        "bairro": "Centro",
        "cidade": "Cidade Teste",
        "estado": "ST",
        "cep": "12345-678",
        "pais": "Brasil",
        'regime_tributario': 'SN',
        'cnae_principal': '6201-5/01',
        'moeda_padrao': 'BRL',
        'senha_certificado': 'senha123',
        'telefone': '(11) 1234-5678',
        'email': 'example@example.com.br',
        'tipo_empresa': 'MATRIZ',
    }
    response = client.post(reverse('empresa:cadastrar_empresa'), data=data)   

    assert response.status_code == 302
    assert Empresa.objects.count() == 1

@pytest.mark.django_db
def test_editar_empresa(client):
    empresa = Empresa.objects.create(
        razao_social="Empresa Teste LTDA",
        nome_fantasia="Empresa Teste",
        cnpj="52.038.391/0001-37",
        inscricao_estadual="123456789",
        inscricao_municipal="987654321",
        logradouro="Rua Teste",
        numero="123",
        complemento="Sala 1",
        bairro="Centro",
        cidade="Cidade Teste",
        estado="ST",
        cep="12345-678",
        pais="Brasil",
        logo="logo.png",
        regime_tributario="SN",
        cnae_principal="6201-5/01",
        moeda_padrao="BRL",
        certificado_digital="certificado.pfx",
        senha_certificado="senha123",
        telefone="(11) 1234-5678",
        email="example@example.com.br",
        tipo_empresa='MATRIZ',
    )
    data = {
        "razao_social": "Empresa Editada LTDA",
        "nome_fantasia": "Empresa Editada",
        "cnpj": "52.038.391/0001-37",
        "inscricao_estadual": "123456789",
        "inscricao_municipal": "987654321",
        "logradouro": "Rua Teste Editada",
        "numero": "456",
        "complemento": "Sala 2",
        "bairro": "Centro Editado",
        "cidade": "Cidade Editada",
        "estado": "ST",
        "cep": "12345-678",
        "pais": "Brasil",
        'regime_tributario': 'SN',
        'cnae_principal': '6201-5/01',
        'moeda_padrao': 'BRL',
        'senha_certificado': 'senha123',
        'telefone': '(11) 1234-5678',
        'email': 'example@example.com.br',
        'tipo_empresa': 'MATRIZ',
    }

    response = client.post(reverse('empresa:editar_empresa', kwargs={'id': empresa.id}), data=data)
   
    assert response.status_code == 302
    empresa.refresh_from_db()
    assert empresa.razao_social == "Empresa Editada LTDA"  
    assert empresa.nome_fantasia == "Empresa Editada"
    assert empresa.logradouro == "Rua Teste Editada"

@pytest.mark.django_db
def test_excluir_empresa(client):   
    empresa = Empresa.objects.create(
        razao_social="Empresa Teste LTDA",
        nome_fantasia="Empresa Teste",
        cnpj="52.038.391/0001-37",
        inscricao_estadual="123456789",
        inscricao_municipal="987654321",
        logradouro="Rua Teste",
        numero="123",
        complemento="Sala 1",
        bairro="Centro",
        cidade="Cidade Teste",
        estado="ST",
        cep="12345-678",
        pais="Brasil",
        logo="logo.png",
        regime_tributario="SN",
        cnae_principal="6201-5/01",
        moeda_padrao="BRL",
        certificado_digital="certificado.pfx",
        senha_certificado="senha123",
        telefone="(11) 1234-5678",
        email="example@example.com.br"
    )
    response = client.post(reverse('empresa:excluir_empresa', kwargs={'id': empresa.id}))
    assert response.status_code == 302
    assert Empresa.objects.count() == 0
    
