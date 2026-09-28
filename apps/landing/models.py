from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Section(models.Model):
    title = models.CharField('Название в меню', max_length=100)
    slug = models.SlugField('URL', unique=True, blank=True)
    content = models.TextField('Содержание страницы', blank=True)
    order = models.PositiveIntegerField('Порядок в меню', default=0)
    is_active = models.BooleanField('Показывать в меню', default=True)
    meta_title = models.CharField('Meta Title', max_length=255, blank=True)
    meta_description = models.TextField('Meta Description', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Секция'
        verbose_name_plural = 'Секции'
        ordering = ['order', 'title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('landing:section', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title