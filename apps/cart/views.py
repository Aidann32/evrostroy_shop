from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from apps.catalog.models import Product
from .cart import Cart


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)
    quantity = int(request.POST.get('quantity', 1))

    cart.add(product=product, quantity=quantity)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = _render_cart_fragment(request).content.decode('utf-8')
        return JsonResponse({
            'success': True,
            'cart_html': html,
            'cart_length': len(cart),
            'cart_total': str(cart.get_total_price()),
            'product_name': product.name,
            'product_image': product.image.url if product.image else '',
        })

    return redirect(request.META.get('HTTP_REFERER', '/'))


def _render_cart_fragment(request):
    cart = Cart(request)
    return render(request, '_partial/offcanvas_content.html', {'cart': cart})


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    action = request.POST.get('action')

    current_qty = cart.cart.get(str(product_id), {}).get('quantity', 0)

    if action == 'increase':
        cart.add(product=product, quantity=1)
    elif action == 'decrease':
        if current_qty > 1:
            cart.update(product=product, quantity=current_qty - 1)
        else:
            cart.remove(product)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = _render_cart_fragment(request).content.decode('utf-8')
        return JsonResponse({
            'success': True,
            'cart_html': html,
            'cart_length': len(cart),
            'cart_total': str(cart.get_total_price()),
        })

    return redirect(request.META.get('HTTP_REFERER', '/'))


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = _render_cart_fragment(request).content.decode('utf-8')
        return JsonResponse({
            'success': True,
            'cart_html': html,
            'cart_length': len(cart),
            'cart_total': str(cart.get_total_price()),
        })

    return redirect(request.META.get('HTTP_REFERER', '/'))


@require_POST
def cart_clear(request):
    cart = Cart(request)
    cart.clear()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = _render_cart_fragment(request).content.decode('utf-8')
        return JsonResponse({
            'success': True,
            'cart_html': html,
            'cart_length': 0,
            'cart_total': '0',
        })

    return redirect(request.META.get('HTTP_REFERER', '/'))
