import logging
from functools import wraps

from protocol import make_response

logger = logging.getLogger('decorators')


# определяем функцию журналирования
def logged(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        logger.debug(f'{func.__name__}: {request}')
        return func(request, *args, **kwargs)
    return wrapper

def login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if 'token' not in request:
            return make_response(request, 403, 'Access denied')
        return func(request, *args, **kwargs)
    return wrapper