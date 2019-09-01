# функции отвечающие за валидацию запросов клиента и ответов от сервера

# запрос
def validate_request(raw):
    if 'action' in raw and 'time' in raw:
        return True
    return False


def make_response(request, code, data=None):
    '''
    # ответ нашего сервера
    # code - код ответа(см. msn http codes)
    '''

    return {
        # данные получаем по ключу
        'action': request.get('action'),
        'time': request.get('time'),

        # data - подстрахует нас от подделки данных
        'data': data,
        'code': code
    }

