class OrdersError(Exception):
    pass


class LackOfMoneyError(OrdersError):
    pass


class AlreadyPaidError(OrdersError):
    pass
