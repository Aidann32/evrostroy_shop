from django.core.cache import cache
from django.conf import settings

from apps.catalog.models import Category

CATEGORIES_KEY = 'categories'
CATEGORIES_CACHE_TTL = 60 * 60

def navbar(request):
    categories = cache.get(CATEGORIES_KEY)
    if categories is None:
        categories = Category.objects.all()
        cache.set(CATEGORIES_KEY, categories, CATEGORIES_CACHE_TTL)
    return {CATEGORIES_KEY: categories}

def yandex_metrika(request):
    return {
        'YANDEX_METRIKA_ID': getattr(settings, 'YANDEX_METRIKA_ID', ''),
        'debug': settings.DEBUG,
    }