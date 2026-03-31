from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError

from apps.empresa.forms import EmpresaForm
from .models import Empresa

def listar_empresas(request):
    empresas = Empresa.objects.only("nome_fantasia", "cnpj", "regime_tributario", "ativo").order_by('-criado_em')
    return render(request, 'empresas/listar_empresas.html', {'empresas': empresas})



def cadastrar_empresa(request):
    form = EmpresaForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Empresa cadastrada com sucesso!")
                return redirect('empresa:listar_empresas')
            
            except ValidationError as e:
                form.add_error(None, e)
            except Exception as e:
                form.add_error(None, f"Erro inesperado: {str(e)}")
        else:
            messages.error(request, "Erro ao cadastrar. Favor verificar os dados informados.")

    context = _get_empresa_context(form, data=request.POST if request.method == 'POST' else None)

    return render(request, 'empresas/cad_empresas.html', context)    

def editar_empresa(request, id):
    empresa = get_object_or_404(Empresa, id=id)
    form = EmpresaForm(request.POST or None, request.FILES or None, instance=empresa)

    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Empresa atualizada com sucesso!")
                return redirect('empresa:listar_empresas')
            
            except ValidationError as e:
                form.add_error(None, e)
            except Exception as e:
                form.add_error(None, f"Erro inesperado: {str(e)}")
        else:
            messages.error(request, "Erro ao atualizar. Favor verificar os dados informados.")

    data_context = request.POST if request.method == 'POST' else empresa
    context = _get_empresa_context(form, empresa=empresa, data=data_context)
    return render(request, 'empresas/cad_empresas.html', context)    


def _get_empresa_context(form, empresa=None, data=None):
    return {
       "form": form,
        "empresa": empresa,
        "data": data,
        "regimes": Empresa._meta.get_field('regime_tributario').choices,
        "tipos": Empresa._meta.get_field('tipo_empresa').choices,
        "moedas": Empresa._meta.get_field('moeda_padrao').choices,
        "matrizes": Empresa.objects.filter(tipo_empresa='MATRIZ'),
    }

def excluir_empresa(request, id):
    empresa = get_object_or_404(Empresa, id=id)
    empresa.delete()
    messages.success(request, "Empresa excluída com sucesso!")
    return redirect('empresa:listar_empresas')


