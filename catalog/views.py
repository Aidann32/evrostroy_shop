from django.db.models import Q
from django.shortcuts import render
from .models import Product

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