from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.all_news, name='all_news'),
    path('<slug:slug>/', views.detail, name='detail'),
]