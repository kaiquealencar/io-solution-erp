from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError


class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O usuário deve ter um email")

        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('gerente', 'Gerente'),
        ('funcionario', 'Funcionário'),
    )
     
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='funcionario')

    empresa = models.ForeignKey(
        'empresa.Empresa',
        on_delete=models.CASCADE,
        related_name='usuarios',
        null=True,  
        blank=True
    )

    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=255, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'       
    REQUIRED_FIELDS = []        
       

    def clean(self):
        super().clean()
        if not self.is_superuser and not self.empresa:
            raise ValidationError("A empresa é obrigatória para usuários comuns.")
        

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.email