import math
import socket
import struct
import threading
import pickle
import time
from typing import Optional, Any

from dupes import ObservableTask
import threading

from enum import Enum

def recv_all(sock, n):
    """ Helper function to receive n bytes or return None if EOF is hit """
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

class Server:
    _executing_task: Optional[ObservableTask] = None
    _socket: socket.socket
    _ip: str
    _port: int

    _must_terminate = False

    _commands_queue = []
    INT_LEN = 15

    @property
    def address(self):
        return (self._ip, self._port)

    def terminate(self):
        self._must_terminate = True

    def __init__(self, ip: Optional[str] = None, port: Optional[int] = None):
        self._ip = ip if ip is not None else "0.0.0.0"
        self._port = port if port is not None else 9999

    def launch(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(self.address)
        self._socket.listen(16)

        self._listening_loop()

    def _listening_loop(self):
        while not self._must_terminate:
            client_socket, client_address = self._socket.accept()
            threading.Thread(target=self._handle_client, args=(client_socket,)).start()

    def _handle_client(self, client_socket: socket.socket):
        try:
            request = self.receive_request(client_socket)
            converted_request = request
            result = None

            if isinstance(converted_request, ObservableTask):
                task: ObservableTask = converted_request

                if self._executing_task is None:
                    self._executing_task = task
                    result = task.execute()
                    self._executing_task = None
                else:
                    result = "ERROR. THE SERVER IS BUSY"

            elif isinstance(converted_request, str):
                if converted_request == "GET_PROGRESS":
                    if self._executing_task is not None:
                        result = self._executing_task.progress
                    else:
                        result = -1
            else:
                result = "ERROR. UNKNOWN REQUEST TYPE."

            self.send_response(client_socket, result)
            client_socket.close()

        except:
            client_socket.close()

    def send_response(self, the_socket: socket.socket, raw_response: Any):
        response = pickle.dumps(raw_response)
        the_socket.send(struct.pack('>I', len(response)))
        the_socket.send(response)

    def receive_request(self, the_socket: socket.socket):
        msglen = struct.unpack('>I', the_socket.recv(4))[0]
        response = the_socket.recv(msglen)
        result = pickle.loads(response)

        return result

#
# def handle_client_connection(client_socket):
#     data = client_socket.recv(8192)  # Получение данных
#     task = pickle.loads(data)  # Десериализация данных
#     print(f"Received task: {task}")
#
#     # Обработка задачи
#     result = process_task(task)
#
#     # Сериализация и отправка результата обратно клиенту
#     response = pickle.dumps(result)
#     response_len = pickle.dumps(len(response))
#     client_socket.send(response_len)
#     client_socket.send(response)
#     client_socket.close()
#
#
# def process_task(task: ObservableTask):
#     # Пример обработки: выполняет реверс строки, если это строка
#     return task.execute()
#
#
# def server_loop():
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind(('0.0.0.0', 9999))
#     server.listen(5)  # Макс. количество ожидающих подключений
#     print('Server is listening on port 9999...')
#
#     while True:
#         client_sock, addr = server.accept()
#         print(f"Accepted connection from {addr}")
#         client_handler = threading.Thread(target=handle_client_connection, args=(client_sock,))
#         client_handler.start()
#
# if __name__ == '__main__':
#     server_loop()

if __name__ == '__main__':
    server = Server()
    server.launch()

