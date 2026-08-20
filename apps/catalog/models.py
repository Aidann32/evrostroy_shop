from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Brand(models.Model):
    name = models.CharField('Бренд', max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField('Категория', max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Attribute(models.Model):
    """Справочник характеристик (Полотно, Коробка, Наличник, Цвет и т.д.)"""
    name = models.CharField('Название характеристики', max_length=100, unique=True)
    slug = models.SlugField('URL', unique=True, blank=True)

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('Название', max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField('Описание', blank=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    image = models.ImageField('Изображение', upload_to='products/', blank=True)
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    meta_title = models.CharField(max_length=255, blank=True)      # SEO
    meta_description = models.TextField(blank=True)               # SEO

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_page', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    """
    Дополнительная характеристика конкретного товара.
    Пример: Полотно = Экошпон дуб, Коробка = Телескопическая и т.д.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='attributes',
        verbose_name='Товар'
    )
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        verbose_name='Характеристика'
    )
    value = models.CharField(
        'Значение',
        max_length=255,
        help_text='Например: "Экошпон дуб", "Белый", "900 мм" и т.д.'
    )

    class Meta:
        verbose_name = 'Характеристика товара'
        verbose_name_plural = 'Характеристики товара'
        unique_together = ['product', 'attribute']
        ordering = ['attribute__name']

    def __str__(self):
        return f'{self.attribute.name}: {self.value}'
