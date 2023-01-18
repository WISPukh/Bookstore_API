from django.contrib.admin import ModelAdmin, register

from carts.models import Cart


@register(Cart)
class CartAdmin(ModelAdmin):
    list_display = (
        'user',
        'book',
        'status',
        'order_id',
        'amount',
        'warranty_days',
        'city',
        'address',
        'total_orders_price'
    )
