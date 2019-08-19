'''
повляет на обработчик пользовательского запроса
'''

import zlib


from functools import wraps
'''
wraps - исключит переопределние атрибутов исходной функций
'''

'''
уменьшим объем передаваемого трафика
'''
def compression_middleware(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        byte_request = zlib.decompress(request)
        byte_response = func(byte_request, *args, **kwargs)
        return zlib.compress(byte_response)
    return wrapper

'''
шифрование
'''
def encryption_middleware(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        # decryption text
        byte_response = func(request, *args, **kwargs)
        # encryption text
        return byte_response
    return wrapper
