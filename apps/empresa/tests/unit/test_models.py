import pytest
from django.core.exceptions import ValidationError
from apps.empresa.models import Empresa


@pytest.mark.django_db
class TestEmpresaModel:

    def test_criar_empresa_sucesso(self, empresa_teste):
        assert Empresa.objects.count() == 1
        assert empresa_teste.razao_social == "I/O Solution LTDA"
        assert str(empresa_teste) == "I/O Solution LTDA"

    def test_editar_empresa_sucesso(self, empresa_teste):
        empresa_teste.razao_social = "I/O Solution LTDA - Editada"
        empresa_teste.save()

        empresa_banco = Empresa.objects.get(id=empresa_teste.id)
        assert empresa_banco.razao_social == "I/O Solution LTDA - Editada"


    def test_cnpj_unico(self, empresa_teste):
        with pytest.raises(Exception):
            Empresa.objects.create(
                razao_social="I/O Solution LTDA",
                cnpj=empresa_teste.cnpj,
                logradouro="avenida Brasil",
                numero="531",
                bairro="Vila Antonio Augusto",
                cidade="Caçapava",
                estado="SP",
                cep="122966-23",
                email="suporte@iosolution.com",
                regime_tributario = "SN"
            )

    def test_validar_campo_vazio(self, empresa_teste):
        empresa = Empresa(razao_social="", cnpj="123")
        
        with pytest.raises(Exception):
            empresa.full_clean()

    def test_matriz_de_outra_matriz(self, empresa_teste):
        empresa_invalida = Empresa(
            razao_social="I/O Solution LTDA",
            cnpj="79.800.500/0001-68",
            logradouro="avenida Brasil",
            numero="531",
            bairro="Vila Antonio Augusto",
            cidade="Caçapava",
            estado="SP",
            cep="122966-23",
            email="suporte@iosolution.com",
            regime_tributario = "SN",
            matriz=empresa_teste        
        )

        with pytest.raises(ValidationError) as excinf:
            empresa_invalida.full_clean()

        assert "matriz" in excinf.value.message_dict
        assert excinf.value.message_dict["matriz"] == ["Matriz não pode ter outra matriz."]

