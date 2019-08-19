import pytest
from datetime import datetime

from protocol import make_response


# static property
# вызываем декоратор
@pytest.fixture
def action_fixture():
    return 'test_action'

@pytest.fixture
def time_fixture():
    return datetime.now().timestamp()

@pytest.fixture
def data_fixture():
    return 'message'

@pytest.fixture
def code_fixture():
    return 200

@pytest.fixture
def request_fixture(action_fixture, time_fixture, data_fixture):
    return {
        'action': action_fixture,
        'time': time_fixture,
        'data': data_fixture,
    }


''' 
# окружение для тестирования, код который ниже можно убрать после внесения fixture
TIME = datetime.now().timestamp()

CODE = 200

REQUEST = {
    'action': 'test',
    'time': TIME,
    'data': 'message'
}

# ожидаемый объект
RESPONSE = {
        'action': 'test',
        'time': TIME,
        'data': 'message',
        'code': CODE
}
'''

'''
# тест-функция
def test_valid_make_response():
    # формируем результат функции make_response
    response = make_response(REQUEST, CODE, 'message')
    assert response.get('code') == CODE
'''

# переписываем функцию исходя из fixture
def test_valid_make_response(request_fixture, data_fixture, code_fixture):
    response = make_response(request_fixture, code_fixture, data_fixture)
    assert response.get('code') == code_fixture



'''
$ pytest
$ pytest server

$ pytest --cov server
$ pytest --cov-report term-missing --cov server
'''