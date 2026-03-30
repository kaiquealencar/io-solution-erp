from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Usuario
from apps.empresa.models import Empresa
from .services import salvar_usuario
from .email_validator import verificar_duplicidade_no_banco


def lista_usuarios(request):
    usuarios = Usuario.objects.only("nome", "email", "role", "is_active").order_by('-date_joined')
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})


def cad_usuario(request):
    empresa_ativa = Empresa.objects.filter(ativo=True).first()

    if request.method == 'POST':
        fields_form = _get_form_field(request)      
       
        try:        
            salvar_usuario(**fields_form, empresa=empresa_ativa)                        
            messages.success(request, f"Usuário: {fields_form['email']} cadastrado com sucesso!")
            
            return redirect('usuarios:lista_usuarios')
        except ValueError as e:
            messages.error(request, str(e))

            return render(request, 'usuarios/cad_usuario.html',
                          {'email': fields_form['email'],
                           'nome': fields_form['nome'],
                            'role': fields_form['role'], 
                            'ativo': fields_form['ativo']}
                    )


    return render(request, 'usuarios/cad_usuario.html')


def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)    
    empresa_ativa = Empresa.objects.filter(ativo=True).first()

    if request.method == 'POST':
        fields_form = _get_form_field(request)           
              
        try:
            salvar_usuario(**fields_form, empresa=empresa_ativa, usuario_id=usuario.id)
            messages.success(request, f"Usuário {usuario.email} atualizado com sucesso!")
            return redirect('usuarios:lista_usuarios')
        except ValueError as e:
            messages.error(request, str(e))
            return render(request, 'usuarios/cad_usuario.html', {'usuario': usuario, **fields_form})


    return render(request, 'usuarios/cad_usuario.html', {'usuario': usuario})


def excluir_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    usuario.delete()
    messages.success(request, f"Usuário {usuario.email} excluído com sucesso!")
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

def _get_form_field(request):
    email = request.POST.get("email")    
    nome = request.POST.get("nome")
    password = request.POST.get("password")
    role = request.POST.get("role")
    val = request.POST.get("is_active")
    ativo = val in ['on', 'True', True]


    return {
        "email": email,
        "nome": nome,
        "password": password,
        "role": role,
        "ativo": ativo
    }
