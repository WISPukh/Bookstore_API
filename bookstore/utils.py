from functools import wraps
from typing import Callable

from rest_framework.response import Response

from bookstore.exceptions import ExceptionBase


def handle_user_exceptions(func: Callable):
    """
    This decorator allows raising errors inside code and return response with description of an error

    Yes. Just like in FastAPI
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ExceptionBase as exc:
            return Response(
                status=exc.status_code,
                data={
                    'error': exc.details
                }
            )

    return wrapper
