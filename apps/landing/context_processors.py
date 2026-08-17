from django.core.cache import cache

from apps.catalog.models import Category

CATEGORIES_KEY = 'categories'
CATEGORIES_CACHE_TTL = 60 * 60

def navbar(request):
    categories = cache.get(CATEGORIES_KEY)
    if categories is None:
        categories = Category.objects.all()
        cache.set(CATEGORIES_KEY, categories, CATEGORIES_CACHE_TTL)
    return {CATEGORIES_KEY: categories}