import socket
import subprocess
import threading
import time
from typing import Optional, Any

from dupes import ObservableTask
from .utilities import send_data, receive_data
from dupes.exceptions import NoPortsAvailableError, ServerNotStartedError


class Server:
    _executing_task: Optional[ObservableTask] = None
    _socket: socket.socket
    _ip: str
    _port: int

    _must_terminate = False

    _commands_queue = []
    _process: subprocess.Popen


    @property
    def address(self):
        return self._ip, self._port

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
            request = receive_data(client_socket)
            converted_request = request
            result = None

            if isinstance(converted_request, ObservableTask):
                task: ObservableTask = converted_request

                if self._executing_task is None:
                    self._executing_task = task
                    try:
                        result = task.execute()
                    except Exception as err:
                        print(err)
                        result = -1
                    self._executing_task = None
                else:
                    result = "ERROR. THE SERVER IS BUSY"

            elif isinstance(converted_request, str):
                if converted_request == "GET_PROGRESS":
                    if self._executing_task is not None:
                        result = self._executing_task.progress
                    else:
                        result = -1
                if converted_request == "IS_ALIVE":
                    result = True
                if converted_request == "TERMINATE":
                    self._socket.close()
                    self._must_terminate = True


            else:
                result = "ERROR. UNKNOWN REQUEST TYPE."

            send_data(client_socket, result)
            client_socket.close()

        except Exception as error:
            print(error)
            client_socket.close()
