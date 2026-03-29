from django.core.exceptions import ValidationError
from django.apps import apps


def verificar_duplicidade_no_banco(email, app_name, model_name):
    usuario_model = apps.get_model(app_name, model_name)

    if usuario_model.objects.filter(email=email).exists():
        raise ValidationError(f"E-mail já cadastrado: {email}")
    
