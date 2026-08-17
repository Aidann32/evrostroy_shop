from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def product_list(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.filter(is_active=True)

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(brand__name__icontains=query)
        )

    return render(request, 'catalog/product_list.html', {
        'products': products,
        'query': query,
    })

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)
    return render(request, 'catalog/product_list.html', {
        'category': category,
        'products': products,
    })