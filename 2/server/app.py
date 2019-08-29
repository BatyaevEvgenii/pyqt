import select
import logging
import threading

# for connection
from socket import socket


class Application:
    def __init__(self, host, port, buffersize, handler):
        self._host = host
        self._port = port
        self._handler = handler
        self._buffersize = buffersize

        self._sock = None
        self._requests = list()
        self._connections = list()

    def __enter__(self):
        if not self._sock:
            self._sock = socket()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        message = 'Сервер выключен...'
        if exc_type:
            if not exc_type is KeyboardInterrupt:
                message = 'Сервер остановлен с ошибкой'
        logging.info(message)
        return True

    def bind(self, backlog=5):
        if not self._sock:
            self._sock = socket()
        self._sock.bind((self._host, self._port,))
        # неблокирующий сервер, но setblocking хорош только не для windows
        self._sock.settimeout(0)
        self._sock.listen(backlog)

    def accept(self):
        try:
            client, address = self._sock.accept()
        except Exception:
            pass
        else:
            # реализуем накопление клиентских подключений
            self._connections.append(client)
            logging.info(f'Клиент подключился: {address[0]}:{address[1]} | Подключений: {self._connections}')

    def read(self, sock):
        try:
            bytes_request = sock.recv(self._buffersize)
        except Exception:
            self._connections.remove(sock)
        else:
            if bytes_request:
                self._requests.append(bytes_request)

    def write(self, sock, response):
        try:
                sock.send(response)
        except Exception:
            self._connections.remove(sock)

    def run(self):
        # ожидание клиентского подключения

        logging.info(f'Сервер запущен... {self._host}:{self._port}')

        while True:
            self.accept()
            # определение типа подключения
            rlist, wlist, xlist = select.select(
                self._connections, self._connections, self._connections, 0
            )
            # алгоритм обработки запросов
            for r_client in rlist:
                # расспаралеливаем чтение
                r_thread = threading.Thread(
                    target=self.read, args=(r_client,)
                )
                r_thread.start()
            # отправка сообщений
            if self._requests:
                byte_request = self._requests.pop()
                byte_response = self._handler(byte_request)

                for w_client in wlist:
                    w_thread = threading.Thread(
                        target=self.write, args=(w_client, byte_response)
                    )
                    w_thread.start()

class CustomApplication(Application):
    def read(self, sock):
        print('Test')
        super(CustomApplication, self).read(sock)