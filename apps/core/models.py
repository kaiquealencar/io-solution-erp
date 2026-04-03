from django.db import models

class ModelBase(models.Model):
    empresa = models.ForeignKey(
        "empresa.Empresa",
        on_delete=models.CASCADE,
        verbose_name="Empresa",
        related_name="%{class}s_set"
    )

    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")

    class Meta:
        abstract = True
