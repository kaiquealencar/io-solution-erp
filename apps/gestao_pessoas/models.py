from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group, Permission
from django.conf import settings
from django.utils import timezone
from datetime import date


class LocalTrabalho(models.Model):
    nome = models.CharField(max_length=100, help_text="Sede, Filial, Home Office")
    endereco = models.CharField(max_length=255)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=4)
    cep = models.CharField(max_length=12)
    tipo = models.CharField(max_length=50, choices=[("intern", "Interno"), ("extern", "Externo"), ("remote", "Home Office")])

    def __str__(self):
        return f"{self.nome} - {self.cidade} / {self.estado}"
    
class Cargo(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    grupo_vinculado = models.OneToOneField(Group, on_delete=models.PROTECT)

    def __str__(self):
        return self.nome
    
    
class Funcionario(models.Model):
    usuario_auth = models.OneToOneField(settings.AUTH_USER_MODEL,
                                         on_delete=models.SET_NULL, 
                                         null=True, 
                                         blank=True, 
                                         related_name="perfil_funcionario")
    class Genero(models.TextChoices):
        PREFIRO_NAO_INFORMAR = "PREFIRO_NAO_INFORMAR", "Prefiro não informar"
        MULHER = "MULHER", "Mulher"
        HOMEM = "HOMEM", "Homem"
        TRAVESTI = "TRAVESTI", "Travesti"
        NAO_BINARIO = "NAO_BINARIO", "Não Binário"
        AGENERO = "AGENERO", "Agênero"
        INTERSEXO = "INTERSEXO", "Intersexo"    

    class PeriocidadePagto(models.TextChoices):
        SEMANAL = "SEMANAL", "Semanal"
        QUINZENAL = "QUINZENAL", "Quinzenal"
        MENSAL = "MENSAL", "Mensal"

    class TipoContrato(models.TextChoices):
        INDERTERMINADO = "INDETERMINADO", "Indeterminado"
        DETERMINADO = "DETERMINADO", "Determinado"
        EXPERIENCIA = "EXPERIENCIA", "Experiência"
        TEMPORARIO = "TEMPORARIO", "Temporário"
        INTERMITENTE = "INTERMITENTE", "Intermitente"
        ESTAGIO = "ESTAGIO", "Estágio"

    #Dados Pessoais      
    nome = models.CharField(max_length=200, verbose_name="Nome")
    cpf = models.CharField(max_length=14, unique=True, verbose_name="Cadastro de Pessoa Física (CPF)")
    rg = models.CharField(max_length=10, verbose_name="Registro Geral (RG)")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    nacionalidade = models.CharField(max_length=100, verbose_name="Nacionalidade")
    naturalidade = models.CharField(max_length=100, verbose_name="Natrualidade")
    nome_mae = models.CharField(max_length=200, verbose_name="Nome da Mãe")
    nome_pai = models.CharField(max_length=200, blank=True, verbose_name="Nome do Pai")
    genero = models.CharField(max_length=30, 
                              choices=Genero.choices, 
                              default=Genero.PREFIRO_NAO_INFORMAR,
                              blank=True,
                              null=False,
                              verbose_name="Gênero")
    ctps_digital = models.CharField(max_length=14   , unique=True, verbose_name="CTPS Digital (CPF)")
    titulo_eleitoral = models.CharField(max_length=14, blank=True, null=True)
    certificado_reservista = models.CharField(max_length=20, blank=True, null=True, verbose_name="Certificado Reservista")
    pis_pasep_nis = models.CharField(max_length=14, verbose_name="PIS/PASEP/NIS")

    #Dados Contratuais

    data_admissao = models.DateField(verbose_name="Data de Admissão")
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT, verbose_name="Cargo")
    salario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Salário Base")
    perido_pagamento = models.CharField(max_length=12, 
                                        choices=PeriocidadePagto.choices, 
                                        default= PeriocidadePagto.MENSAL,
                                        verbose_name= "Periocidade do Pagamento"
                                        )
    tipo_contrato = models.CharField(max_length=20,
                                     choices=TipoContrato.choices,
                                     default=TipoContrato.INDERTERMINADO,
                                     verbose_name="Tipo de Contrato")
    jornada_trabalho_dia_semana = models.CharField(max_length=10)
    jornada_trabalho_hora_entrada = models.TimeField()
    jornada_trabalho_hora_saida = models.TimeField()
    local_trabalho = models.ForeignKey(LocalTrabalho, on_delete=models.PROTECT)

    
    #Dados Complementares - ASO
    tipo_aso = models.CharField(max_length=100, 
                                choices=[("A", "Admissional"), 
                                         ("P", "Periódico"), 
                                         ("R", "Retorno ao trabalho"),
                                         ("M", "Mudança de Risco"),
                                         ("D", "Demissional")], verbose_name="Tipo do ASO")
    data_realizacao_aso = models.DateField(verbose_name="Data da realização do exame ASO")
    parecer = models.CharField(max_length=8, choices=[("APTO", "Apto"), ("INAPTO", "Inapto")], verbose_name="Parecer Médico")
    nome_medico = models.CharField(max_length=200, verbose_name="Nome do Médico")
    numero_crm = models.CharField(max_length=7, verbose_name="Número Conselhor Regional de Medicina (CRM)")
    uf_crm = models.CharField(max_length=2, verbose_name="UF - CRM")
    data_vencimento_aso = models.DateField(verbose_name="Data de Vencimento ASO")
    foto_exame = models.FileField(upload_to="gestao_pessoas/ASOS", blank=True, null=True)

    #Dados Complementares - Escolaridade    
    comprovante_escolaridade = models.FileField(upload_to="gestao_pessoas/comprovante_escolaridade", blank=True, null=True)

    #Dados Complementares - Conta Bancária
    banco = models.CharField(max_length=100, verbose_name="Banco")
    agencia = models.CharField(max_length=15, verbose_name="Agência Bancária")
    conta = models.CharField(max_length=20, verbose_name="Conta")
    tipo_conta = models.CharField(max_length=20, choices=[("CORRENTE", "Corrente"), ("POUPANCA", "Poupança")])
    titular_conta = models.CharField(max_length=100, verbose_name="Titular da Conta")
    cpf_cnpj_conta = models.CharField(max_length=20, verbose_name="CPF ou CNPJ da Conta")

    #Dados Complementares - vale Transporte
    declaracao_vale_transporte = models.FileField(upload_to="gestao_pessoas/vale_transporte", blank=True, null=True)



    #Dados Complementares - Dependente
    tem_dependentes = models.BooleanField(default=False)

    def clean(self):
        if not self.data_nascimento:
            return 

        hoje = timezone.now().date()
        nasc = self.data_nascimento
        idade = hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))

        if self.genero == self.Genero.HOMEM and 18 <= idade <= 45:
            if not self.certificado_reservista:
                raise ValidationError({
                    "certificado_reservista": (
                        f"O funcionário tem  {idade} anos e é do gênero masculino."
                        "O certificado de reservista é obrigatório nesse caso"
                    )
                })


    def __str__(self):
        return f"{self.nome} - {self.cargo.nome}"
    
class Dependente(models.Model):     
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name="dependentes")
    nome_dependente = models.CharField(max_length=200, verbose_name="Nome do dependente")
    cpf_dependente = models.CharField(max_length=14, unique=True, verbose_name="Cadastro de Pessoa Física (CPF) - Dependente")
    data_nascimento_dependente = models.DateField(verbose_name="Data de Nascimento - Dependente")

    def __str__(self):
        return f"{self.nome_dependente} (Dep. de  {self.funcionario.nome})"


    




