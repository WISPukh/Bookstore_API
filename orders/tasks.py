import pdb

from celery import shared_task
from django.core.mail import send_mail

from bookstore.settings import EMAIL_HOST_USER
from carts.models import Cart


@shared_task
def order_created(order_id):
    order = Cart.objects.filter(orders_id=order_id).first()
    if order:
        pdb.set_trace()
        return send_mail('Order nr. {}'.format(order_id),
                         'Dear {},\n\n'
                         'Your order has been successfully created'
                         'Your order\'s link is http://127.0.0.1:1337/api/order/detail/?orders_id={} .'
                         .format(order.user.email,
                                 order_id),
                         EMAIL_HOST_USER,
                         [order.user.email])
