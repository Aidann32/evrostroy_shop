from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<str:slug>/', views.category_products, name='category_products'),
    path('product/<str:slug>/', views.product_page, name='product_page'),
    path('categories/', views.all_categories, name='all_categories'),
]