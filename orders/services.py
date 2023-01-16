from django.db.transaction import atomic

from orders import errors
from users.models import User


class OrderService:

    def list(self, user_pk, model, *args, **kwargs):
        users_orders = model.objects.filter(
            user_id=user_pk,
            status__in=[
                'AWAITING_ARRIVAL',
                'AWAITING_PAYMENT',
                'PAID',
                'AWAITING_DELIVERY',
                'SENT',
                'FINISHED'
            ]
        )
        data_to_serialize = []
        order_ids = list((users_orders.values('order_id').distinct('order_id')))
        for order_id in order_ids:
            data_to_serialize.append(model.objects.get_total_orders_information(
                user_pk, order_id['order_id']
            ))

        return data_to_serialize

    def list_detail(self, order_id, model, user_pk):
        return model.objects.get_total_orders_information(
            user_pk=user_pk, order_id=order_id
        )

    @atomic
    def pay(self, user_pk, order_id, model):
        users_orders = model.objects.filter(
            order_id=order_id, status='AWAITING_PAYMENT')
        if not users_orders.exists():
            raise errors.AlreadyPaidError("This order already has been paid or await arriving")

        user = User.objects.get(id=user_pk)
        users_orders_detail = model.objects.get_total_orders_information(
            user_pk, order_id
        )
        if user.balance < users_orders_detail['persons_discounted_price']:
            raise errors.LackOfMoneyError("You dont have enough money to pay for this order")

        user.balance -= users_orders_detail['persons_discounted_price']
        user.save()
        users_orders.update(
            status='PAID'
        )
        return True
