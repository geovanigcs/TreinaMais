from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import uuid


class Category(models.Model):
    """Modelo para categorias de produtos"""
    name = models.CharField('Nome', max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField('Descrição', blank=True)
    is_active = models.BooleanField('Ativo', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Brand(models.Model):
    """Modelo para marcas"""
    name = models.CharField('Nome', max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField('Descrição', blank=True)
    is_active = models.BooleanField('Ativo', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """Modelo principal de produtos"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Nome', max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField('Descrição')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField('Preço', max_digits=10, decimal_places=2)
    sale_price = models.DecimalField('Preço Promocional', max_digits=10, decimal_places=2, null=True, blank=True)
    stock_quantity = models.PositiveIntegerField('Quantidade em Estoque', default=0)
    is_active = models.BooleanField('Ativo', default=True)
    is_featured = models.BooleanField('Destaque', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})

    @property
    def current_price(self):
        """Retorna o preço atual (promocional ou normal)"""
        return self.sale_price if self.sale_price else self.price

    @property
    def is_on_sale(self):
        """Verifica se o produto está em promoção"""
        return bool(self.sale_price and self.sale_price < self.price)

    @property
    def discount_percentage(self):
        """Calcula a porcentagem de desconto"""
        if self.is_on_sale:
            return int(((self.price - self.sale_price) / self.price) * 100)
        return 0

    @property
    def is_in_stock(self):
        """Verifica se o produto está em estoque"""
        return self.stock_quantity > 0


class ProductImage(models.Model):
    """Modelo para imagens dos produtos"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Imagem', upload_to='products/')
    is_main = models.BooleanField('Imagem Principal', default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Imagem do Produto'
        verbose_name_plural = 'Imagens dos Produtos'
        ordering = ['-is_main', 'created_at']

    def __str__(self):
        return f"Imagem de {self.product.name}"
