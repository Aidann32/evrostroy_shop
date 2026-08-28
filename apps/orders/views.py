import re
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from urllib.parse import quote

from apps.cart.cart import Cart
from .models import Order, OrderItem


def clean_kz_phone(phone: str) -> str | None:
    digits = re.sub(r'\D', '', phone)

    if digits.startswith('8') and len(digits) == 11:
        digits = '7' + digits[1:]

    if len(digits) != 11 or not digits.startswith('7'):
        return None

    valid_codes = {
        '700', '701', '702', '703', '704', '705', '706', '707', '708', '709',
        '747', '750', '751', '760', '761', '762', '763', '764',
        '771', '775', '776', '777', '778',
    }

    operator_code = digits[1:4]
    if operator_code not in valid_codes:
        return None

    return digits


@require_POST
def checkout(request):
    cart = Cart(request)

    if not cart or len(cart) == 0:
        messages.error(request, 'Корзина пуста')
        return redirect('index')

    phone_raw = request.POST.get('phone', '').strip()
    comment = request.POST.get('comment', '').strip()

    phone = clean_kz_phone(phone_raw)

    if not phone:
        messages.error(request, 'Введите корректный казахстанский номер телефона')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    order = Order.objects.create(
        phone=phone,          # сохраняем уже очищенный: 77001234567
        comment=comment,
        total=cart.get_total_price()
    )

    for item in cart:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            quantity=item['quantity'],
            price=item['price']
        )

    lines = [
        f"Новый заказ №{order.order_number}",
        f"Телефон: +{phone}",
        "",
        "Состав заказа:",
    ]

    for item in order.items.select_related('product'):
        lines.append(
            f"• {item.product.name} × {item.quantity} = {item.price * item.quantity} ₸"
        )

    lines.append("")
    lines.append(f"Итого: {order.total} ₸")

    if comment:
        lines.append("")
        lines.append(f"Комментарий: {comment}")

    message = "\n".join(lines)

    cart.clear()

    manager_phone = "77089817618"

    whatsapp_url = f"https://wa.me/{manager_phone}?text={quote(message)}"

    return redirect(whatsapp_url)