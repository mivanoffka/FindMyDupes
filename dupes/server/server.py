import logging
import socket
import subprocess
import threading
import time
from typing import Optional, Any

from dupes import ObservableTask
from dupes.exceptions import NoPortsAvailableError, ServerNotStartedError
import pickle
import socket
import struct
from typing import Any
from logger import Logger


class Server:
    _executing_task: Optional[ObservableTask] = None
    _socket: socket.socket
    _ip: str
    _port: int
    _logger: Logger

    _must_terminate = False

    _commands_queue = []
    _process: subprocess.Popen

    def send_data(self, the_socket: socket.socket, raw_response: Any):
        if self._must_terminate:
            return -1

        response = pickle.dumps(raw_response)
        response_length = len(response)

        the_socket.send(struct.pack('>Q', response_length))
        the_socket.send(response)

    def receive_data(self, the_socket: socket.socket):
        if self._must_terminate:
            return -1

        request_length = struct.unpack('>Q', the_socket.recv(8))[0]
        response = the_socket.recv(request_length)

        return pickle.loads(response)

    @property
    def address(self):
        return self._ip, self._port

    def terminate(self):
        self._must_terminate = True

    def __init__(self, ip: Optional[str] = None, port: Optional[int] = None):
        self._ip = ip if ip is not None else "0.0.0.0"
        self._port = port if port is not None else 9999
        self._logger = Logger("app/logs/server")

    def launch(self):
        self._logger.setup()

        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.bind(self.address)
            self._socket.listen(16)
        except Exception as error:
            logging.error(f"Failed to bind to {self._ip}:{self._port}: {error}")

        logging.info("Server started on {}".format(self._port))
        self._listening_loop()

    def _listening_loop(self):
        while not self._must_terminate:
            try:
                client_socket, client_address = self._socket.accept()
                threading.Thread(target=self._handle_client, args=(client_socket,)).start()
            except:
                pass

    def _handle_client(self, client_socket: socket.socket):
        logging.info("Accepted client connection.")

        try:
            request = self.receive_data(client_socket)

            if request == -1:
                return

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
                        result = err
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

            result = self.send_data(client_socket, result)
            if result == -1:
                return

            client_socket.close()

        except Exception as error:
            print(error)
            client_socket.close()
