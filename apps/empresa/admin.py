from django.contrib import admin
from apps.empresa.models import Empresa

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("nome_fantasia", "cnpj", "regime_tributario", "ativo")
    list_filter = ("ativo", "regime_tributario", "estado")
    search_fields = ("nome_fantasia", "razao_social", "cnpj")

    @admin.display(description="Nome Fantasia")
    def nome_fantasia(self, obj):
        return obj.nome_fantasia or ""
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_action(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        
        return actions

