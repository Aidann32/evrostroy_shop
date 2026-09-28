from decimal import Decimal
from django.conf import settings
from apps.catalog.models import Product

from copy import deepcopy
from decimal import Decimal


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),  # ← обязательно str()
                'name': product.name,
                'image': product.image.url if product.image else '',
                'slug': product.slug,
            }

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart and quantity > 0:
            self.cart[product_id]['quantity'] = quantity
            self.save()
        elif quantity <= 0:
            self.remove(product)

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        products_map = {str(p.id): p for p in products}

        for product_id, item_data in self.cart.items():
            item = item_data.copy()  # важная копия
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            item['product'] = products_map.get(product_id)
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )