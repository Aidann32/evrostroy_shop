import uuid
from django.db import models

class Order(models.Model):
    order_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # GUID
    phone = models.CharField('Телефон', max_length=20, blank=True)
    comment = models.TextField('Комментарий', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    # статус можно добавить позже (new, processing и т.д.)

    def __str__(self):
        return str(self.order_number)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('apps.catalog.Product', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # цена на момент заказа

    def __str__(self):
        return f'{self.product.name} × {self.quantity}'