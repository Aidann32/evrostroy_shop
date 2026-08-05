from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class News(models.Model):
    title = models.CharField('Заголовок', max_length=255)
    slug = models.SlugField('URL', unique=True, blank=True)
    preview = models.TextField('Краткое описание', blank=True)
    content = models.TextField('Содержание')
    image = models.ImageField('Изображение', upload_to='news/', blank=True)
    is_published = models.BooleanField('Опубликовано', default=True)
    published_at = models.DateTimeField('Дата публикации', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-published_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title