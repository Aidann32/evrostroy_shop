from django.contrib import admin
from .models import Brand, Category, Product


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price', 'is_active', 'created_at')
    list_filter = ('brand', 'category', 'is_active', 'created_at')
    search_fields = ('name', 'brand__name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'is_active')
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'brand', 'category', 'description', 'price', 'image', 'is_active')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Служебная информация', {
            'fields': ('created_at',),
        }),
    )