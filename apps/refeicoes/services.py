
import calendar
from datetime import date
from django.utils.timezone import now


def filtro_refeicoes_dia(request, RefeicaoDia, quinzena=None, mes=None):
    hoje = now().date()

    quinzena, mes = quinzena, mes
    
    ano, mes_num = map(int, mes.split('-')) if mes else (hoje.year, hoje.month)
    ultimo_dia = calendar.monthrange(ano, mes_num)[1]

    match quinzena:
        case '1':
            inicio = date(ano, mes_num, 1)
            fim = date(ano, mes_num, 15)
        case '2':
            inicio = date(ano, mes_num, 16)
            fim = hoje if mes_num == hoje.month and ano == hoje.year else date(ano, mes_num, ultimo_dia)
        case _:
             if hoje.day <= 16:
                inicio = date(ano, mes_num, 1)
                fim = date(ano, mes_num, 15)
             else:
                inicio = date(ano, mes_num, 1)
                fim = date(ano, mes_num, ultimo_dia)            

    refeicoes_dias = (
        RefeicaoDia.objects
        .filter(data__range=(inicio, fim))
        .select_related('refeicao')
        .order_by('-data')

    )

    return refeicoes_dias, inicio, fim, quinzena, mes