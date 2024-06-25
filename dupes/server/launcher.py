import socket
import subprocess
import threading
import time
from typing import Optional, Any

from dupes import ObservableTask
from .utilities import send_data, receive_data
from dupes.exceptions import NoPortsAvailableError, ServerNotStartedError
from py_singleton import singleton


@singleton
class InternalServer:
    _process: subprocess.Popen
    _port: int = -1
    _MAX_IS_ALIVE_ATTEMPTS = 6

    def is_port_in_use(self, port, host='127.0.0.1'):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((host, port))
            except socket.error:
                return True
            return False

    def launch_process(self):
        ports_to_try = (i for i in range(7800, 7900))

        for port_to_try in ports_to_try:
            if not self.is_port_in_use(port=port_to_try):
                self._port = port_to_try
                break

        if self._port == -1:
            raise NoPortsAvailableError("No ports available in range [7800, 7899]")

        self._process = subprocess.Popen(["python", "server_script.py", str(self._port)])

        for i in range(0, self._MAX_IS_ALIVE_ATTEMPTS):
            try:
                self.communicate_with("IS_ALIVE")
            except Exception as error:
                if i >= self._MAX_IS_ALIVE_ATTEMPTS - 1:
                    raise ServerNotStartedError()
                else:
                    time.sleep(0.5)
                continue
            break

    def communicate_with(self, data: Any, big_timeout=False):
        result = (None, )

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', self._port))
        if big_timeout:
            client.settimeout(99999)

        send_data(client, data)

        result = receive_data(client)

        client.close()

        return result
