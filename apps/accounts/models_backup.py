from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Modelo customizado de usuário"""
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Address(models.Model):
    """Modelo para endereços dos usuários"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    label = models.CharField(max_length=50, default='Casa')
    street = models.CharField('Rua', max_length=255)
    number = models.CharField('Número', max_length=10)
    complement = models.CharField('Complemento', max_length=100, blank=True)
    neighborhood = models.CharField('Bairro', max_length=100)
    city = models.CharField('Cidade', max_length=100)
    state = models.CharField('Estado', max_length=2)
    zip_code = models.CharField('CEP', max_length=10)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'

    def __str__(self):
        return f"{self.label} - {self.street}, {self.number} - {self.city}/{self.state}"

    def save(self, *args, **kwargs):
        if self.is_default:
            # Define todos os outros endereços do usuário como não padrão
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)
