from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
import uuid


class Category(MPTTModel):
    """Modelo para categorias de produtos com hierarquia"""
    name = models.CharField('Nome', max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField('Descrição', blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image = models.ImageField('Imagem', upload_to='categories/', blank=True)
    is_active = models.BooleanField('Ativo', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:category', kwargs={'slug': self.slug})


class Brand(models.Model):
    """Modelo para marcas"""
    name = models.CharField('Nome', max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField('Descrição', blank=True)
    logo = models.ImageField('Logo', upload_to='brands/', blank=True)
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
    short_description = models.CharField('Descrição Curta', max_length=500)
    description = RichTextField('Descrição Completa')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    sku = models.CharField('SKU', max_length=50, unique=True)
    price = models.DecimalField('Preço', max_digits=10, decimal_places=2)
    sale_price = models.DecimalField('Preço Promocional', max_digits=10, decimal_places=2, null=True, blank=True)
    stock_quantity = models.PositiveIntegerField('Quantidade em Estoque', default=0)
    weight = models.DecimalField('Peso (kg)', max_digits=5, decimal_places=3, null=True, blank=True)
    dimensions = models.CharField('Dimensões (CxLxA)', max_length=50, blank=True)
    is_active = models.BooleanField('Ativo', default=True)
    is_featured = models.BooleanField('Destaque', default=False)
    tags = TaggableManager()
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
    def main_image(self):
        """Retorna a imagem principal do produto"""
        image = self.images.filter(is_main=True).first()
        return image.image if image else None

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
    alt_text = models.CharField('Texto Alternativo', max_length=255, blank=True)
    is_main = models.BooleanField('Imagem Principal', default=False)
    order = models.PositiveIntegerField('Ordem', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Imagem do Produto'
        verbose_name_plural = 'Imagens dos Produtos'
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"Imagem de {self.product.name}"

    def save(self, *args, **kwargs):
        if self.is_main:
            # Define todas as outras imagens do produto como não principal
            ProductImage.objects.filter(product=self.product, is_main=True).update(is_main=False)
        super().save(*args, **kwargs)


class ProductAttribute(models.Model):
    """Modelo para atributos dos produtos (cor, tamanho, etc.)"""
    name = models.CharField('Nome', max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Atributo'
        verbose_name_plural = 'Atributos'

    def __str__(self):
        return self.name


class ProductAttributeValue(models.Model):
    """Modelo para valores dos atributos"""
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, related_name='values')
    value = models.CharField('Valor', max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Valor do Atributo'
        verbose_name_plural = 'Valores dos Atributos'
        unique_together = ['attribute', 'value']

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


class ProductVariant(models.Model):
    """Modelo para variantes dos produtos"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    sku = models.CharField('SKU da Variante', max_length=50, unique=True)
    price = models.DecimalField('Preço', max_digits=10, decimal_places=2, null=True, blank=True)
    stock_quantity = models.PositiveIntegerField('Quantidade em Estoque', default=0)
    is_active = models.BooleanField('Ativo', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Variante do Produto'
        verbose_name_plural = 'Variantes dos Produtos'

    def __str__(self):
        return f"{self.product.name} - {self.sku}"

    @property
    def current_price(self):
        """Retorna o preço da variante ou do produto pai"""
        return self.price if self.price else self.product.current_price


class ProductVariantAttribute(models.Model):
    """Modelo para relacionar variantes com atributos"""
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='attributes')
    attribute_value = models.ForeignKey(ProductAttributeValue, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Atributo da Variante'
        verbose_name_plural = 'Atributos das Variantes'
        unique_together = ['variant', 'attribute_value']

    def __str__(self):
        return f"{self.variant} - {self.attribute_value}"


class Review(models.Model):
    """Modelo para avaliações dos produtos"""
    RATING_CHOICES = [
        (1, '1 Estrela'),
        (2, '2 Estrelas'),
        (3, '3 Estrelas'),
        (4, '4 Estrelas'),
        (5, '5 Estrelas'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField('Avaliação', choices=RATING_CHOICES)
    title = models.CharField('Título', max_length=255)
    comment = models.TextField('Comentário')
    is_approved = models.BooleanField('Aprovado', default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
        unique_together = ['product', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} - {self.rating} estrelas"
