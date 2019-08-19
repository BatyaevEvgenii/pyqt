import json
import logging


from resolvers import resolve
from middlewares import (compression_middleware, encryption_middleware)
from protocol import (validate_request, make_response)

'''
такая реализация:
1 позволит навешивать дополнительные обработчики
2 возможность навешивания middleware обработчика(как пример: ограниченный трафик)
'''

@compression_middleware
@encryption_middleware
def handle_default_request(raw_request):
    # в строку потом в словарь
    request = json.loads(raw_request.decode())

    # проходим валидацию
    if validate_request(request):
        action_name = request.get('action')
        # извлекаем контроллер
        controller = resolve(action_name)
        # if action == 'echo':
        if controller:
            try:
                ''' фиксируем debug '''
                logging.debug(f'Controller {action_name} resolved with request: {request}')
                # print(f'Controller {action_name} resolved with request: {request}')

                response = controller(request)
            except Exception as err:
                ''' фикусируем критическую ситуацию '''
                logging.critical(f'Controller {action_name} error: {err}')
                # print(f'Controller {action_name} error: {err}')
                response = make_response(request, 500, 'Internal server error')
        else:
            ''' фиксируем симантические ошибки '''
            logging.error(f'Controller {action_name} not found')
            # print(f'Controller {action_name} not found')
            response = make_response(request, 404, f'Action with name "{action_name}"   not supported')
    else:
        ''' фиксируем симантические ошибки '''
        logging.error(f'Controller wrong request: {request}')
        # print(f'Controller wrong request: {request}')
        response = make_response(request, 400, 'Wrong request format!')

    return json.dumps(response).encode()