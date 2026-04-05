from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from apps.empresa import forms
from .models import Usuario
from apps.empresa.models import Empresa
from .services import salvar_usuario
from .email_validator import verificar_duplicidade_no_banco
from .forms import UsuarioForm, LoginForm

class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'usuarios/login.html'



@login_required
def lista_usuarios(request):
    queryset = Usuario.objects.all()

    if not request.user.is_superuser:
        queryset = queryset.filter(empresa_id=request.user.empresa_id)

    
    usuarios = queryset.only(
        "nome",
        "email",
        "role",
        "is_active"
    ).order_by("-date_joined")

    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})

@login_required
def cad_usuario(request):  
    empresa_vinculada = request.user.empresa if request.user.empresa else Empresa.objects.filter(ativo=True).first()
    forms = UsuarioForm(request.POST or None, empresa=empresa_vinculada)

    if request.method == 'POST':   
        if forms.is_valid():
            try:
                forms.save()        

                messages.success(request, f"Usuário: {forms.cleaned_data['email']} cadastrado com sucesso!")
                return redirect('usuarios:lista_usuarios')
            except ValueError as e:
                messages.error(request, str(e))
        else:
            print(f"ERROS DO FORMULÁRIO: {forms.errors.as_data()}")
            messages.error(request, "Por favor, preencha todos os campos corretamente.")

    context = _get_usuario_context(
        forms, 
        email=request.POST.get("email"), 
        nome=request.POST.get("nome"), 
        role=request.POST.get("role"), 
        ativo=request.POST.get("is_active"),
        data=request.POST
    )
    
    return render(request, 'usuarios/cad_usuario.html', context)

@login_required
def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id, empresa=request.user.empresa)    
    empresa_vinculada = request.user.empresa or usuario.empresa
    forms = UsuarioForm(request.POST or None, instance=usuario, empresa=empresa_vinculada)       

    if request.method == 'POST':           
        if forms.is_valid():
            try:
                forms.save()
                messages.success(request, f"Usuário {usuario.email} atualizado com sucesso!")
                return redirect('usuarios:lista_usuarios')
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        messages.error(request, f"Erro no campo {field}: {error}")
        else:
            messages.error(request, "Erro ao atualizar. Verifique os campos!")

    context = _get_usuario_context(
        forms, 
        email= forms["email"].value() or usuario.email, 
        nome=forms["nome"].value() or usuario.nome, 
        role=forms["role"].value() or usuario.role, 
        ativo=forms["is_active"].value(),
        data=request.POST if request.method == 'POST' else None
    )

    return render(request, 'usuarios/cad_usuario.html', context)

@login_required
def excluir_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id, empresa=request.user.empresa)

    if request.method == "POST":
        email_salvo = usuario.email
        usuario.delete()
        messages.success(request, f"Usuário {email_salvo} excluído com sucesso!")
        return redirect('usuarios:lista_usuarios')

    return redirect('usuarios:lista_usuarios')


def validar_email(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)

        if not email:
            return JsonResponse({"error": "Email é obrigatório."}, status=400)
        
        try:
            verificar_duplicidade_no_banco(email, 'usuarios', 'Usuario')
            return JsonResponse({"valid": True})
        
        except Exception as e:
            return JsonResponse({"valid": False, "error": str(e)}, status=200)
    
    return JsonResponse({"error": "Método não permitido."}, status=405)



def _get_usuario_context(forms, email=None, nome=None, role=None, ativo=None, data=None):
   return {
        "forms": forms,
        "email": email,
        "nome": nome,
        "role_selecionado": role, 
        "ativo": ativo,
        "data": data,
        "role_choices": Usuario._meta.get_field('role').choices,
    }


