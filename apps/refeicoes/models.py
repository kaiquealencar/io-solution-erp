from django.db import models


class Refeicoes(models.Model):
    TIPO = [
        ("PACIENTE_ACOMPANHANTE", "Paciente e Acompanhante"),
        ("PACIENTE_DIETA_LIQUIDA", "Paciente Dieta Líquida"),
        ("PACIENTE_BEBIDA", "Paciente Bebida"),
        ("FUNCIONARIOS", "Funcionários")
    ]

    nome = models.CharField(max_length=255, blank=True, null=True)
    tipo = models.CharField(max_length=30, choices=TIPO, blank=True, null=True)

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"
    

class RefeicaoDia(models.Model):
    empresa = models.ForeignKey(
        'empresa.Empresa',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    data = models.DateField()
    refeicao = models.ForeignKey(Refeicoes, on_delete=models.CASCADE, related_name='refeicoes_dia')
    quantidade = models.PositiveIntegerField(default=0) 

  
    def __str__(self):
        return f"{self.refeicao} - {self.data} - Quantidade: {self.quantidade}"