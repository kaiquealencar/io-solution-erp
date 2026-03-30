from django.core.exceptions import ValidationError
from django.apps import apps


def verificar_duplicidade_no_banco(email, app_name, model_name, usuario_id=None):
    usuario_model = apps.get_model(app_name, model_name)
    query = (usuario_model.objects
             .filter(email=email)
             .exclude(id=usuario_id) if usuario_id else usuario_model.objects.filter(email=email))   

    if query.exists():
        raise ValidationError(f"E-mail já cadastrado: {email}")
    
