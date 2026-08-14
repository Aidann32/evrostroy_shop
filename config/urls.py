from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from config import settings

urlpatterns = [
    path('', include('apps.landing.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
