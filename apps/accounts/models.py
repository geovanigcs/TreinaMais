from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Modelo customizado de usuário"""
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Address(models.Model):
    """Modelo para endereços dos usuários"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    street = models.CharField('Rua', max_length=255)
    city = models.CharField('Cidade', max_length=100)
    state = models.CharField('Estado', max_length=2)
    zip_code = models.CharField('CEP', max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'

    def __str__(self):
        return f"{self.street} - {self.city}/{self.state}"
