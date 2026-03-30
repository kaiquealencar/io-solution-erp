from django.db import transaction
from .models import Usuario
from .email_validator import verificar_duplicidade_no_banco


def salvar_usuario(email, nome, password, role, ativo, empresa, usuario_id=None):
    
    verificar_duplicidade_no_banco(email, 'usuarios', 'Usuario', usuario_id)    

    with transaction.atomic():        
        if usuario_id:
            try:
                usuario = Usuario.objects.get(id=usuario_id)
            except Usuario.DoesNotExist:
                raise ValueError(f'Usuário com id {usuario_id} não encontrado.')

            usuario.email = email
            usuario.nome = nome

            if password:
                usuario.set_password(password)
           
            usuario.role = role
            usuario.is_active = ativo
            usuario.empresa = empresa
            usuario.save()
        else:        
            usuario = Usuario.objects.create_user(
                email=email,
                nome=nome,
                password=password,
                role=role,
                is_active=ativo,
                empresa=empresa
            )           

        return usuario