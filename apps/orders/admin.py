from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'phone', 'total', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('order_number', 'phone')
    readonly_fields = ('order_number', 'created_at', 'total')
    inlines = [OrderItemInline]

    fieldsets = (
        ('Информация о заказе', {
            'fields': ('order_number', 'phone', 'comment', 'total', 'created_at')
        }),
    )