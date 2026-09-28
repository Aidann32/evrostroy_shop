from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from urllib.parse import quote

from .models import Product, Category

def product_list(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.filter(is_active=True)

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(brand__name__icontains=query)
        )

    return render(request, 'catalog/category_products.html', {
        'products': products,
        'query': query,
    })

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)
    return render(request, 'catalog/category_products.html', {
        'category': category,
        'products': products,
    })

def product_page(request, slug):
    product = get_object_or_404(Product.objects.prefetch_related('attributes__attribute'), slug=slug, is_active=True)
    product_url = request.build_absolute_uri(product.get_absolute_url())
    message = (
        f"Здравствуйте, пишу из сайта Еврострой, "
        f"у меня есть вопрос по данному товару: {product_url}"
    )
    return render(request, 'catalog/product_page.html', {
        'product': product,
        'whatsapp_text': quote(message),
    })

def all_categories(request):
    categories = Category.objects.all()
    return render(request, 'catalog/categories.html', {
        'categories': categories,
    })