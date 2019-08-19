 # server
# for connection
from socket import socket

# обработка командной строки
import yaml
import json
import logging
import select
import threading
from argparse import ArgumentParser

# из нашего модуля protocol импортируем
from protocol import validate_request, make_response

from handlers import handle_default_request

from resolvers import resolve


def read(sock, connections, requests, buffersize):
    try:
        bytes_request = sock.recv(buffersize)
    except Exception:
        connections.remove(sock)
    else:
        if bytes_request:
            requests.append(bytes_request)

def write(sock, connections, response):
    try:
        sock.send(response)
    except Exception:
        connections.remove(sock)

# конструктор объекта
parser = ArgumentParser()

# конфигурируем
parser.add_argument(
    # внутри описание того что будем парсить
    # shortcut, имя конфигурационного файла, тип аргумента
    '-c', '--config', type=str,
    # аргумент опционален(запуск со стандартными настройками), за что отвечает(help text)
    required=False, help='установки пути конфига'
)
'''
if __name__ == '__main__': можем убрать после того как файл переименовали в __main__,
тем самым перевели python на модульное выполнение(директория client)
'''

args = parser.parse_args()

# значение по умолчанию
default_config = {
    'host': 'localhost',
    'port': 8000,
    'buffersize': 1024
}
# host = 'localhost'
# port = 8000

# если в args попал конфиг, то...
if args.config: 
    with open(args.config) as file:
        file_config = yaml.load(file, Loader=yaml.Loader)
        '''
        данные подтянем из конфига $ python server -c config.yaml,
        а если их нет - возьмем из переменных
        host = file_config.get('host', host)
        port = file_config.get('port', port)
        но можем и сделать их "глобальными" значениями по-умолчанию:
        '''
        default_config.update(file_config)

host, port = (default_config.get('host'), default_config.get('port'))

''' блок логирования '''
# logger = logging.getLogger('main')
# logger.setLevel(logging.DEBUG)
#
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#
# handler = logging.FileHandler('main.log')
# handler.setFormatter(formatter)
# handler.setLevel(logging.DEBUG)
#
# logger.addHandler(handler)
''' '''

''' упрощаем журналирование, минуя блок логирования'''
logging.basicConfig(
    level=logging.DEBUG,
    format= '%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('main.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# коллекция хранения клиетских запросов
requests = []

# реализуем накомление клиентских подключений
connections = []

try:
    sock = socket()
    sock.bind((host, port))

    # неблокирующий сервер, но setblocking хорош только не для windows
    # sock.setblocking(False)
    sock.settimeout(0)

    sock.listen(5) # слушаем 5 соединений клиентов

    ''' здесь и далее заменяем все ранее установленные print на logger.info'''
    logging.info(f'Сервер запущен... {host}:{port}')
    # print(f'Сервер запущен... {host}:{port}')

    # ожидание клиентского подключения
    while True:
        try:
            client, address = sock.accept()

            # реализуем накомление клиентских подключений
            connections.append(client)

            logging.info(f'Клиент подключился: {address[0]}:{address[1]} | Подключений: {connections}')
            # print(f'Клиент подключился: {address[0]}:{address[1]}')
        except :
            pass

        # определение типа подключения
        rlist, wlist, xlist = select.select(
            connections, connections, connections, 0
        )


        # алгоритм обработки запросов
        for r_client in rlist:
            # расспаралеливаем чтение
            r_thread = threading.Thread(target=read, args=(r_client, connections, requests, default_config.get('buffersize')))
            # byte_request = r_client.recv(default_config.get('buffersize'))
            # requests.append(byte_request)
            r_thread.start()

        # отправка сообщений
        if requests:
            byte_request = requests.pop()
            byte_response = handle_default_request(byte_request)

            for w_client in wlist:
                w_thread = threading.Thread(target=write,
                                            args=(w_client, connections, byte_response))
                w_thread.start()
                # w_client.send(byte_response)




        '''
        переносим вырезанную часть кода в handlers.py и 
        вызовем ее ниже
        '''

        ''' удялем то что ниже так как это использовалось в блокирующем сервере'''
        # byte_request = client.recv(default_config.get('buffersize'))

        # byte_response = handle_default_request(byte_request)

        # client.send(json.dumps(response).encode())
        # client.send(byte_response)

        # не разрываем соединение с клиентом
        # client.close()
        # print(f'Клиент отключился...')

    # обработаем исключение
except KeyboardInterrupt:
    logging.info('Сервер выключен.')
    # print('Сервер выключен.')




'''
python __main__.py -c config.yaml
python __main__.py --help
python client
python server -c config.yaml
fab server
fab client
fab kill
fab client:w
'''

