from django import forms
from django.contrib.auth.forms import AuthenticationForm
from apps.usuarios.email_validator import verificar_duplicidade_no_banco
from .models import Usuario


class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    
    class Meta:
        model = Usuario
        fields = ["nome", "email", "password", "role", "is_active"]

        exclude = [
            'date_joined',      
            'last_login',       
            'is_superuser',     
            'is_staff',         
            'groups',           
            'user_permissions', 
        ]
    
    def __init__(self, *args, **kwargs):

        self.empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)        


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
    
    def clean(self):
        if self.empresa:
            self.instance.empresa = self.empresa
        
        return super().clean()

class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-3 rounded-lg bg-gray-200 mt-2 border focus:border-blue-500 focus:bg-white focus:outline-none',
        'placeholder': 'Seu e-mail'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-3 rounded-lg bg-gray-200 mt-2 border focus:border-blue-500 focus:bg-white focus:outline-none',
        'placeholder': 'Sua senha'
    }))