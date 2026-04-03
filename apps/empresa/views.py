from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

from apps.empresa.forms import EmpresaForm
from .models import Empresa


@login_required
def listar_empresas(request):
    queryset = Empresa.objects.all()

    if not request.user.is_superuser:
        queryset = queryset.filter(id=request.user.empresa.id)


    empresas = queryset.only(
        "razao_social",
        "nome_fantasia",
        "cnpj",
        "regime_tributario",
        "ativo"
    ).order_by("-criado_em")
   # empresas = Empresa.objects.filter(id=request.user.empresa.id).only(
   #     "razao_social",
   #     "nome_fantasia", 
   #     "cnpj", 
   #     "regime_tributario", 
   #     "ativo").order_by('-criado_em')
    
    return render(request, 'empresas/listar_empresas.html', {'empresas': empresas})


@login_required
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

    context = _get_empresa_context(request, form, data=request.POST if request.method == 'POST' else None)

    return render(request, 'empresas/cad_empresas.html', context)    

@login_required
def editar_empresa(request, id):
    empresa = get_object_or_404(Empresa, id=id, pk=request.user.empresa.id)
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
    context = _get_empresa_context(request, form, empresa=empresa, data=data_context)
    return render(request, 'empresas/cad_empresas.html', context)    



@login_required
def excluir_empresa(request, id):
    empresa = get_object_or_404(Empresa, id=id, pk=request.user.empresa.id)
    empresa.delete()
    messages.success(request, "Empresa excluída com sucesso!")
    return redirect('empresa:listar_empresas')


def _get_empresa_context(request, form, empresa=None, data=None):
    return {
       "form": form,
        "empresa": empresa,
        "data": data,
        "regimes": Empresa._meta.get_field('regime_tributario').choices,
        "tipos": Empresa._meta.get_field('tipo_empresa').choices,
        "moedas": Empresa._meta.get_field('moeda_padrao').choices,
        "matrizes": Empresa.objects.filter(tipo_empresa='MATRIZ', id=request.user.empresa.id),
    }



