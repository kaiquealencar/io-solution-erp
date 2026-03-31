from django import forms

from apps.usuarios.email_validator import verificar_duplicidade_no_banco
from .models import Usuario


class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    
    class Meta:
        model = Usuario
        fields = "__all__"

        exclude = [
            'date_joined',      
            'last_login',       
            'is_superuser',     
            'is_staff',         
            'groups',           
            'user_permissions', 
        ]
    
    def save(self, commit=True):
        usuario = super().save(commit=False)
        senha = self.cleaned_data.get('password')

        if senha:
            usuario.set_password(senha)
        elif self.instance.pk:
            usuario.password = Usuario.objects.get(pk=self.instance.pk).password

        if commit:
          usuario.save()
        
        return usuario
