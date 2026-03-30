
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.timezone import now

from .models import Refeicoes, RefeicaoDia
from .services import filtro_refeicoes_dia, salvar_refeicao_dia

def listar_refeicoes(request):
    refeicoes = Refeicoes.objects.only("id", "nome", "tipo").order_by('nome')
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
    
    refeicoes_dia, inicio, fim, quinzena, mes = filtro_refeicoes_dia(request, RefeicaoDia, request.GET.get('quinzena'), request.GET.get('mes'))    

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
            try:
                salvar_refeicao_dia(refeicao_id, data, quantidade)
                messages.success(request, 'Refeição do dia cadastrada com sucesso!')
            except ValueError as e:
                messages.error(request, f'Erro {e} - Quantidade inválida. A quantidade deve ser um número positivo.')
                
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

        try:
            salvar_refeicao_dia(request, refeicao_id, data, quantidade, id)
            messages.success(request, 'Refeição do dia atualizada com sucesso!')
            return redirect('refeicoes:listar_refeicoes_dia')
        except ValueError as e:
            messages.error(request, f'Erro {e} - Quantidade inválida. A quantidade deve ser um número positivo.')
            return redirect('refeicoes:editar_refeicao_dia', id=id)       

    refeicoes = Refeicoes.objects.only("id", "nome", "tipo").order_by('nome')
    return render(request, 'refeicoes/cadastrar_refeicoes_dia.html', {
        'refeicoes': refeicoes, 
        'refeicao_dia': refeicao_dia}
    )

def excluir_refeicao_dia(request, id): 
    refeicao_dia = get_object_or_404(RefeicaoDia, id=id)
    refeicao_dia.delete()
    messages.success(request, 'Refeição do dia excluída com sucesso!')
    return redirect('refeicoes:listar_refeicoes_dia')



