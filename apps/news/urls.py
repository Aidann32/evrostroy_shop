from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.news_list, name='list'),
    path('<str:slug>/', views.detail, name='detail'),
]