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

    def test_excluir_empresa_inativacao(self, empresa_teste):
        id_empresa = empresa_teste.id

        empresa_teste.delete()
        empresa_banco = Empresa.objects.get(id=id_empresa)

        assert Empresa.objects.count() == 1
        assert empresa_banco.ativo is False
        assert empresa_banco.razao_social == "I/O Solution LTDA"

    def test_inativar_empresa_desativa_usuarios_vinculados(self, empresa_teste):
        from apps.usuarios.models import Usuario
        
        usuario = Usuario.objects.create_user(
            email="test_cascade@io.com",
            nome="test_cascade",
            password="123",
            empresa=empresa_teste,
            is_active=True
        )

        empresa_teste.delete()
        usuario.refresh_from_db()

        assert usuario.is_active is False
