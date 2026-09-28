from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap

from apps.catalog.sitemaps import ProductSitemap, CategorySitemap

from config import settings

admin.site.site_header = "Еврострой - панель управления"
admin.site.site_title = "Админка"
admin.site.index_title = "Добро пожаловать в админ-панель"

sitemaps = {
    'products': ProductSitemap,
    'categories': CategorySitemap,
}

urlpatterns = [
    path('', include('apps.landing.urls')),
    path('admin/', admin.site.urls),
    path('news/', include('apps.news.urls')),
    path('catalog/', include('apps.catalog.urls')),
    path('cart/', include('apps.cart.urls', namespace='cart')),
    path('orders/', include('apps.orders.urls')),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path('404/', TemplateView.as_view(template_name='404.html'), name='404'),
    ]
