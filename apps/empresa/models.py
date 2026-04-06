from django.db import models
from django.core.exceptions import ValidationError
from .validator import validar_cnpj
from .utils import somente_numeros

class Empresa(models.Model):
    REGIME_TRIBUTARIO_CHOICES = [
        ('SN', 'Simples Nacional'),
        ('LP', 'Lucro Presumido'),
        ('LR', 'Lucro Real'),
    ]

    TIPO_EMPRESA_CHOICES = [
        ('MATRIZ', 'Matriz'),
        ('FILIAL', 'Filial'),
    ]

    MOEDA_CHOICES = [
        ('BRL', 'Real Brasileiro'),
        ('USD', 'Dólar Americano'),
        ('EUR', 'Euro'),
    ]

    razao_social = models.CharField(max_length=255)
    nome_fantasia = models.CharField(max_length=255, blank=True, null=True)
    cnpj = models.CharField(max_length=18, unique=True, validators=[validar_cnpj])
    inscricao_estadual = models.CharField(max_length=20, blank=True, null=True)
    inscricao_municipal = models.CharField(max_length=20, blank=True, null=True)
    cnae_principal = models.CharField(max_length=20, blank=True, null=True)
    logo = models.ImageField(upload_to='empresas/logos/', blank=True, null=True)
    moeda_padrao = models.CharField(max_length=3, choices=MOEDA_CHOICES, default='BRL')
    certificado_digital = models.FileField(upload_to='empresas/certificados/', blank=True, null=True)
    senha_certificado = models.CharField(max_length=255, blank=True, null=True)
    
    logradouro = models.CharField(max_length=255)    
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    complemento = models.CharField(max_length=255, blank=True, null=True)    
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=10)
    pais = models.CharField(max_length=100, default='Brasil')

    email = models.EmailField()
    telefone = models.CharField(max_length=20, blank=True, null=True)


    regime_tributario = models.CharField(
        max_length=2,
        choices=REGIME_TRIBUTARIO_CHOICES
    )

    tipo_empresa = models.CharField(
        max_length=10,
        choices=TIPO_EMPRESA_CHOICES,
        default='MATRIZ'
    )

    matriz = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='filiais'
    )

    ativo = models.BooleanField(default=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()

        if self.cnpj:
            self.cnpj = somente_numeros(self.cnpj)

        if self.cep:
            cep = somente_numeros(self.cep)
            if len(cep) != 8:
                raise ValidationError({'cep': 'CEP deve conter 8 dígitos.'})
            self.cep = cep

        if self.tipo_empresa == 'MATRIZ' and self.matriz:
            raise ValidationError({
                'matriz': 'Matriz não pode ter outra matriz.'
            })
        
        if self.tipo_empresa == 'FILIAL' and not self.matriz:
            raise ValidationError({
                'matriz': 'Filial deve estar vinculada a uma matriz.'
            })


    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):                
        self.ativo = False
        self.save()
        self.usuarios.update(is_active=False)
        
    def __str__(self):
        return self.nome_fantasia or self.razao_social