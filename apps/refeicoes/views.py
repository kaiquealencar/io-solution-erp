import calendar
from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.timezone import now

from .models import Refeicoes, RefeicaoDia

def listar_refeicoes(request):
    refeicoes = Refeicoes.objects.all()
    return render(request, 'refeicoes/listar_refeicoes.html', {'refeicoes': refeicoes})

def cadastrar_refeicao(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        tipo = request.POST.get('tipo')

        if nome and tipo:
            Refeicoes.objects.create(nome=nome, tipo=tipo)
            messages.success(request, 'Refeição cadastrada com sucesso!')
            return redirect('refeicoes:listar_refeicoes')
        else:
            messages.error(request, 'Por favor, preencha todos os campos.')

    return render(request, 'refeicoes/cadastrar_refeicao.html')


def editar_refeicao(request, id):
    refeicao = get_object_or_404(Refeicoes, id=id)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        tipo = request.POST.get('tipo')

        if nome and tipo:
            refeicao.nome = nome
            refeicao.tipo = tipo
            refeicao.save()
            messages.success(request, 'Refeição atualizada com sucesso!')
            return redirect('refeicoes:listar_refeicoes')
        else:
            messages.error(request, 'Por favor, preencha todos os campos.')

    return render(request, 'refeicoes/cadastrar_refeicao.html', {'refeicao': refeicao})

def excluir_refeicao(request, id):
    refeicao = get_object_or_404(Refeicoes, id=id)
    refeicao.delete()
    messages.success(request, 'Refeição excluída com sucesso!')
    return redirect('refeicoes:listar_refeicoes')


def listar_refeicoes_dia(request):
    
    refeicoes_dia, inicio, fim, quinzena, mes = _filtro_refeicoes_dia(request)

    context = {
        'refeicoes_dia': refeicoes_dia,
        'inicio': inicio,
        'fim': fim,
        'quinzena': quinzena,
        'mes': mes or now().strftime('%Y-%m'),
    }

    return render(request, 'refeicoes/listar_refeicoes_dia.html', context)

def cadastrar_refeicao_dia(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        refeicao_id = request.POST.get('refeicao')
        quantidade = request.POST.get('quantidade')

        if all([data, refeicao_id, quantidade]):
            refeicao = get_object_or_404(Refeicoes, id=refeicao_id)
            RefeicaoDia.objects.create(data=data, refeicao=refeicao, quantidade=quantidade)
            messages.success(request, 'Refeição do dia cadastrada com sucesso!')
            return redirect('refeicoes:listar_refeicoes_dia')
        else:
            messages.error(request, 'Por favor, preencha todos os campos.')

    refeicoes = Refeicoes.objects.all()
    return render(request, 'refeicoes/cadastrar_refeicoes_dia.html', {'refeicoes': refeicoes})

def editar_refeicao_dia(request, id):
    refeicao_dia = get_object_or_404(RefeicaoDia, id=id)

    if request.method == 'POST':
        data = request.POST.get('data')
        refeicao_id = request.POST.get('refeicao')
        quantidade = request.POST.get('quantidade')

        if data and refeicao_id and quantidade:
            refeicao = get_object_or_404(Refeicoes, id=refeicao_id)
            refeicao_dia.data = data
            refeicao_dia.refeicao = refeicao
            refeicao_dia.quantidade = quantidade
            refeicao_dia.save()
            messages.success(request, 'Refeição do dia atualizada com sucesso!')
            return redirect('refeicoes:listar_refeicoes_dia')
        else:
            messages.error(request, 'Por favor, preencha todos os campos.')

    refeicoes = Refeicoes.objects.all()
    return render(request, 'refeicoes/cadastrar_refeicoes_dia.html', {'refeicoes': refeicoes, 'refeicao_dia': refeicao_dia})

def excluir_refeicao_dia(request, id): 
    refeicao_dia = get_object_or_404(RefeicaoDia, id=id)
    refeicao_dia.delete()
    messages.success(request, 'Refeição do dia excluída com sucesso!')
    return redirect('refeicoes:listar_refeicoes_dia')


def _filtro_refeicoes_dia(request):
    hoje = now().date()

    quinzena = request.GET.get('quinzena') or None  
    mes = request.GET.get('mes')
    
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
             if hoje.day <= 15:
                inicio = date(ano, mes_num, 1)
                fim = date(ano, mes_num, 15)
             else:
                inicio = date(ano, mes_num, 1)
                fim = date(ano, mes_num, ultimo_dia)            

    refeicoes_dias = (
        RefeicaoDia.objects
        .filter(data__gte=inicio, data__lte=fim)
        .select_related('refeicao')
        .order_by('data')

    )

    return refeicoes_dias, inicio, fim, quinzena, mes
