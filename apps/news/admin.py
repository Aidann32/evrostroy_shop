from django.contrib import admin
from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'published_at')
    list_filter = ('is_published', 'published_at')
    search_fields = ('title', 'preview', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_published',)
    readonly_fields = ('published_at', 'updated_at')

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'preview', 'content', 'image', 'is_published')
        }),
        ('Даты', {
            'fields': ('published_at', 'updated_at'),
        }),
    )