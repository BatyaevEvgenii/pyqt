 # client
# обработка командной строки
import zlib
import yaml
import json
import hashlib
import threading
from datetime import datetime
from socket import socket
from argparse import ArgumentParser

def read(sock, buffersize):
    while True:
        compressed_response = sock.recv(buffersize)
        byte_response = zlib.decompress(compressed_response)
        print(f'{byte_response.decode()}')

# конструктор объекта
parser = ArgumentParser()

# конфигурируем
parser.add_argument(
    '-c', '--config', type=str,
    required=False, help='установки пути конфига'
)

args = parser.parse_args()

# значение по умолчанию
default_config = {
    'host': 'localhost',
    'port': 8000,
    'buffersize': 1024
}

# если в args попал конфиг, то...
if args.config:
    with open(args.config) as file:
        file_config = yaml.load(file, Loader=yaml.Loader)
        default_config.update(file_config)



sock = socket()
sock.connect(
    (default_config.get('host'), default_config.get('port'))
)

print(f'Клиент запущен... ')


# бесконечный цикл, пока клиент не уйдет сам
try:
    read_thread = threading.Thread(target=read, args=(sock, default_config.get('buffersize')))
    read_thread.start()
    while True:
        # генерация хэша
        hash_obj = hashlib.sha256()
        hash_obj.update(
            str(datetime.now().timestamp()).encode()
        )

        action = input('Введите действие: ')
        data = input('Введите данные: ')

        # запрос клиента
        # сгенерирует токен на основе timestamp
        request = {
            'action': action,
            # timestamp поможет нам с отображением даты в дальнейшем
            'time': datetime.now().timestamp(),
            'data': data,
            'token': hash_obj.hexdigest()
        }

        # строковое представление запроса
        string_request = json.dumps(request)

        byte_request = zlib.compress(string_request.encode())
        # print(byte_request)
        # формируем байтовую последовательность
        sock.send(byte_request)
        print(f'Клиент отправил данные: {data}')


except KeyboardInterrupt:
    sock.close()
    print('Клиент вышел...')


'''
python __main__.py -c config.yaml
python __main__.py --help
python client
python client -c config.yaml
fab client:w
'''
