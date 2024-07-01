import pickle
import socket
import struct
import subprocess
import sys
import time
from typing import Any

from config import BASE_DIR
from dupes.exceptions import NoPortsAvailableError, ServerNotStartedError
from .singleton import Singleton


class InternalServerManager(metaclass=Singleton):

    """
    Allows you to launch and communicate with an instance of INTERNAL SERVER in a separate process
    """

    _process: subprocess.Popen
    _port: int = -1
    _MAX_IS_ALIVE_ATTEMPTS = 6

    def _launch_script(self):
        self._process = subprocess.Popen([sys.executable, str(BASE_DIR / "server/script.py"), str(self._port)])

    def _send_data(self, the_socket: socket.socket, raw_response: Any):
        response = pickle.dumps(raw_response)
        response_length = len(response)

        the_socket.send(struct.pack('>Q', response_length))
        the_socket.send(response)

    def _receive_data(self, the_socket: socket.socket):
        request_length = struct.unpack('>Q', the_socket.recv(8))[0]
        response = the_socket.recv(request_length)

        return pickle.loads(response)

    def _is_port_in_use(self, port, host='127.0.0.1'):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((host, port))
            except socket.error:
                return True
            return False

    def launch(self):
        ports_to_try = (i for i in range(7800, 7900))

        for port_to_try in ports_to_try:
            if not self._is_port_in_use(port=port_to_try):
                self._port = port_to_try
                break

        if self._port == -1:
            raise NoPortsAvailableError("No ports available in range [7800, 7899]")

        self._launch_script()

        for i in range(0, self._MAX_IS_ALIVE_ATTEMPTS):
            try:
                self.communicate_with("IS_ALIVE")
            except Exception as error:
                if i >= self._MAX_IS_ALIVE_ATTEMPTS - 1:
                    raise ServerNotStartedError("No information can be provided here. Go to server logs.")
                else:
                    time.sleep(0.5)
                continue
            break

        return self._port

    def communicate_with(self, data: Any, big_timeout=False, dont_wait_for_response=False):
        result = (None, )

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', self._port))
        if big_timeout:
            client.settimeout(99999)

        self._send_data(client, data)
        if dont_wait_for_response:
            client.close()
            return

        result = self._receive_data(client)

        client.close()

        return result
