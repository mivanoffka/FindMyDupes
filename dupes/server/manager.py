import pickle
import socket
import struct
import subprocess
import threading
import time
from pathlib import Path
from typing import Optional, Any

from dupes import ObservableTask
from dupes.exceptions import NoPortsAvailableError, ServerNotStartedError
from .singleton import Singleton

from config import BASE_DIR
import sys

import os
import sys
import ctypes
import subprocess
from pathlib import Path
import platform

class InternalServer(metaclass=Singleton):
    _process: subprocess.Popen
    _port: int = -1
    _MAX_IS_ALIVE_ATTEMPTS = 6

    def start_script(self):
        match platform.system():
            case "Windows":
                if not ctypes.windll.shell32.IsUserAnAdmin():

                    script = os.path.abspath(sys.argv[0])
                    params = ' '.join([str(Path(__file__).parent / "script.py"), str(self._port)])
                    try:
                        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'{script} {params}', None, 1)
                    except Exception as e:
                        print(f"Failed to elevate privileges: {e}")
                else:
                    self._process = subprocess.Popen(
                        [sys.executable, str(Path(__file__).parent / "script.py"), str(self._port)])

            case "Darwin" | "Linux":
                self._process = subprocess.Popen([sys.executable,
                                                  str(Path(__file__).parent / "script.py"), str(self._port)])

    def send_data(self, the_socket: socket.socket, raw_response: Any):
        response = pickle.dumps(raw_response)
        response_length = len(response)

        the_socket.send(struct.pack('>Q', response_length))
        the_socket.send(response)

    def receive_data(self, the_socket: socket.socket):
        request_length = struct.unpack('>Q', the_socket.recv(8))[0]
        response = the_socket.recv(request_length)

        return pickle.loads(response)

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

        #command = f'runas /user:Administrator "{sys.executable}  {str(BASE_DIR / "app/script.py")} {str(self._port)}"'
        #self._process = subprocess.Popen(command, shell=True)

        self.start_script()

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

        self.send_data(client, data)

        result = self.receive_data(client)

        client.close()

        return result
