from urllib.parse import urlsplit

from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.news.models import News
from .models import Product, Category


class BaseSitemap(Sitemap):
    # http/https берем из SITE_URL, иначе из запроса
    protocol = urlsplit(settings.SITE_URL).scheme or None

    def get_domain(self, site=None):
        return urlsplit(settings.SITE_URL).netloc or super().get_domain(site)


class StaticSitemap(BaseSitemap):
    changefreq = 'weekly'

    def items(self):
        return ['main', 'all_categories', 'product_list', 'about', 'contact', 'news:list']

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0 if item == 'main' else 0.6


class ProductSitemap(BaseSitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Product.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at


class CategorySitemap(BaseSitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Category.objects.all()


class NewsSitemap(BaseSitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return News.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at
