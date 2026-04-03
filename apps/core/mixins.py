from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class EmpresaFilterMixin(LoginRequiredMixin):
    
    def get_queryset(self):
        
        queryset = super().get_queryset()
        user = self.request.user 

        if user.is_superuser:
            return queryset
        
        if not hasattr(user, "empresa") or user.empresa is None:
            raise PermissionDenied("Usuário não possui empresa vinculada.")
    
        return queryset.filter(empresa=user.empresa)
    
    def form_valid(self, form):
        user = self.request.user
    
        if not user.is_superuser:
            form.instance.empresa = user.empresa
    
        return super().form_valid(form)


