from django.db import models
from django.conf import settings
import uuid


class Cart(models.Model):
    """Modelo para carrinho de compras"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='carts')
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Carrinho'
        verbose_name_plural = 'Carrinhos'

    def __str__(self):
        return f"Carrinho {self.id}"

    @property
    def total_items(self):
        """Retorna o total de itens no carrinho"""
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        """Retorna o subtotal do carrinho"""
        return sum(item.total_price for item in self.items.all())

    @property
    def total_weight(self):
        """Retorna o peso total do carrinho"""
        return sum(item.total_weight for item in self.items.all())

    def clear(self):
        """Remove todos os itens do carrinho"""
        self.items.all().delete()


class CartItem(models.Model):
    """Modelo para itens do carrinho"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Item do Carrinho'
        verbose_name_plural = 'Itens do Carrinho'
        unique_together = ['cart', 'product']

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    @property
    def unit_price(self):
        """Retorna o preço unitário do item"""
        return self.product.current_price

    @property
    def total_price(self):
        """Retorna o preço total do item"""
        return self.unit_price * self.quantity

    @property
    def total_weight(self):
        """Retorna o peso total do item"""
        if self.product.weight:
            return self.product.weight * self.quantity
        return 0


class Coupon(models.Model):
    """Modelo para cupons de desconto"""
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Porcentagem'),
        ('fixed', 'Valor Fixo'),
    ]

    code = models.CharField('Código', max_length=50, unique=True)
    description = models.CharField('Descrição', max_length=255)
    discount_type = models.CharField('Tipo de Desconto', max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField('Valor do Desconto', max_digits=10, decimal_places=2)
    minimum_amount = models.DecimalField('Valor Mínimo', max_digits=10, decimal_places=2, default=0)
    usage_limit = models.PositiveIntegerField('Limite de Uso', null=True, blank=True)
    used_count = models.PositiveIntegerField('Quantidade Usada', default=0)
    is_active = models.BooleanField('Ativo', default=True)
    valid_from = models.DateTimeField('Válido de')
    valid_until = models.DateTimeField('Válido até')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cupom'
        verbose_name_plural = 'Cupons'

    def __str__(self):
        return self.code

    def is_valid(self, cart_total=0):
        """Verifica se o cupom é válido"""
        from django.utils import timezone
        now = timezone.now()
        
        if not self.is_active:
            return False, "Cupom inativo"
        
        if now < self.valid_from or now > self.valid_until:
            return False, "Cupom fora do período de validade"
        
        if self.usage_limit and self.used_count >= self.usage_limit:
            return False, "Cupom esgotado"
        
        if cart_total < self.minimum_amount:
            return False, f"Valor mínimo de R$ {self.minimum_amount} não atingido"
        
        return True, "Cupom válido"

    def calculate_discount(self, cart_total):
        """Calcula o desconto do cupom"""
        if self.discount_type == 'percentage':
            return (cart_total * self.discount_value) / 100
        else:
            return min(self.discount_value, cart_total)
