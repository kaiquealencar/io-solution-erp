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
    empresa = get_object_or_404(Empresa, id=id)
    form = EmpresaForm(request.POST or None, request.FILES or None, instance=empresa)

    if not request.user.is_superuser:
        if request.user.empresa is None or request.user.empresa.id != empresa.id:
            messages.error(request, "Acesso negado: Você não tem permissão para editar esta empresa.")
            return redirect('empresa:listar_empresas')

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
    empresa = get_object_or_404(Empresa, id=id)

    if request.user.empresa and request.user.empresa.id == empresa.id:
        messages.error(request, "Operação negada: você não pode excluir a própria empresa onde está logado.")
        return redirect('empresa:listar_empresas')

    if request.method == "POST":
        empresa.delete()

        messages.success(request, "Empresa excluída com sucesso!")
        return redirect('empresa:listar_empresas')

    return redirect('empresa:listar_empresas')


def _get_empresa_context(request, form, empresa=None, data=None):
    qs = Empresa.objects.filter(tipo_empresa="MATRIZ")
    
    if request.user.is_superuser:
        matrizes = qs
    elif request.user.empresa:
        matrizes = qs.filter(id=request.user.empresa.id)
    else:
        matrizes = qs.none()
    

    context = {       
        "form": form,
        "empresa": empresa,
        "data": data,
        "regimes": Empresa._meta.get_field('regime_tributario').choices,
        "tipos": Empresa._meta.get_field('tipo_empresa').choices,
        "moedas": Empresa._meta.get_field('moeda_padrao').choices,
        "matrizes": matrizes
    }

    return context



