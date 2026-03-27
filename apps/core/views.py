import json
from django.shortcuts import render
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Sum
from apps.refeicoes.models import RefeicaoDia as Refeicao
from apps.empresa.models import Empresa


def index(request):
    hoje = now().date()
    user = request.user
    empresa = getattr(user, 'empresa', None)

    refeicoes_hoje = Refeicao.objects.filter(empresa=empresa, data=hoje).count()
    refeicoes_mes = Refeicao.objects.filter(
        empresa=empresa, data__month=hoje.month, data__year=hoje.year
    ).count()

    labels = []
    valores = []
    detalhes_do_tipo = []
    for i in range(6, -1, -1):
        dia = hoje - timedelta(days=i)        
        labels.append(dia.strftime('%d/%m'))        
        refeicoes_do_dia = Refeicao.objects.filter(empresa=empresa, data=dia)

        total_dia = refeicoes_do_dia.aggregate(total=Sum('quantidade'))['total'] or 0        
        valores.append(total_dia)
        
        nomes_tipos = list(refeicoes_do_dia.values_list('refeicao__nome', flat=True).distinct())

        if nomes_tipos:
            detalhes_do_tipo.append(", ".join(nomes_tipos))
        else:
            detalhes_do_tipo.append("Nenhuma refeição registrada")

    empresas_ativas = Empresa.objects.filter(ativo=True).count()

    ultima_atualizacao_obj = Refeicao.objects.filter(empresa=empresa).order_by('-data').first()
    ultima_atualizacao = ultima_atualizacao_obj.data if ultima_atualizacao_obj else None

    contexto = {
        'refeicoes_hoje': refeicoes_hoje,
        'refeicoes_mes': refeicoes_mes,
        'labels': labels,    
        'valores': valores,  
        'tipos': detalhes_do_tipo,
        'empresas_ativas': empresas_ativas,
        'ultima_atualizacao': ultima_atualizacao,
    }

    return render(request, 'core/index.html', contexto)