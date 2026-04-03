
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required

from .forms import RefeicaoDiaForm
from .models import Refeicoes, RefeicaoDia
from .services import filtro_refeicoes_dia



@login_required
def listar_refeicoes(request):
    refeicoes = Refeicoes.objects.only("id", "nome", "tipo").order_by('nome')
    return render(request, 'refeicoes/listar_refeicoes.html', {'refeicoes': refeicoes})

@login_required
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

@login_required
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

@login_required
def excluir_refeicao(request, id):
    refeicao = get_object_or_404(Refeicoes, id=id)
    refeicao.delete()
    messages.success(request, 'Refeição excluída com sucesso!')
    return redirect('refeicoes:listar_refeicoes')

@login_required
def listar_refeicoes_dia(request):
    quinzena = request.GET.get('quinzena')
    mes = request.GET.get('mes')
    
    refeicoes_dia, inicio, fim, quinzena, mes = filtro_refeicoes_dia(
        request, 
        RefeicaoDia, 
        quinzena, mes
    )    

    context = {
        'refeicoes_dia': refeicoes_dia,
        'inicio': inicio,
        'fim': fim,
        'quinzena': quinzena,
        'mes': mes or now().strftime('%Y-%m'),
    }

    return render(request, 'refeicoes/listar_refeicoes_dia.html', context)

@login_required
def cadastrar_refeicao_dia(request):
    forms = RefeicaoDiaForm(request.POST or None)
    if request.method == 'POST':
        if forms.is_valid():
            try:             
                forms.save()
                messages.success(request, 'Refeição do dia cadastrada com sucesso!')
                return redirect('refeicoes:listar_refeicoes_dia')
            except ValueError as e:
                messages.error(request, f'Erro {e} - Quantidade inválida. A quantidade deve ser um número positivo.')
        else:
            messages.error(request, 'Por favor, preencha todos os campos corretamente.')

    
    context = _get_refeicao_dia_context(
            forms, 
            Refeicoes.objects.only("id", "nome", "tipo").order_by('nome'), 
            data=request.POST)

    return render(request, 'refeicoes/cadastrar_refeicoes_dia.html', context)

@login_required
def editar_refeicao_dia(request, id):
    refeicao_dia = get_object_or_404(RefeicaoDia, id=id)
    form = RefeicaoDiaForm(request.POST or None, instance=refeicao_dia)

    if request.method == "POST":
        if form.is_valid():
            try:               
                form.save()
                messages.success(request, 'Refeição do dia atualizada com sucesso!')
                return redirect('refeicoes:listar_refeicoes_dia')
            except ValueError as e:
                messages.error(request, f'Erro {e} - Quantidade inválida. A quantidade deve ser um número positivo.')
  
    
    refeicoes = Refeicoes.objects.only("id", "nome", "tipo").order_by('nome')  
    context = _get_refeicao_dia_context(
            form, refeicoes, refeicao_dia, data=request.POST if request.method == 'POST' else None)
    
    return render(request, 'refeicoes/cadastrar_refeicoes_dia.html', context)

@login_required
def excluir_refeicao_dia(request, id): 
    refeicao_dia = get_object_or_404(RefeicaoDia, id=id)
    refeicao_dia.delete()
    messages.success(request, 'Refeição do dia excluída com sucesso!')
    return redirect('refeicoes:listar_refeicoes_dia')


def _get_refeicao_dia_context(form, refeicoes=None, refeicao_dia=None, data=None):
    return {
        'form': form,
        'refeicoes': refeicoes,
        'refeicao_dia': refeicao_dia,
        'data': data,
    }
