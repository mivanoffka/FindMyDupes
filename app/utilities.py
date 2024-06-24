from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox

import sys
import traceback

import pickle
import socket
import struct
from typing import Any


def display_message(message: str, title="Сообщение"):
    msgBox = QMessageBox()
    msgBox.setText(title)
    msgBox.setInformativeText(message)
    msgBox.setStandardButtons(QMessageBox.StandardButton.Close)
    msgBox.setWindowIcon(QtGui.QIcon("/Users/mivanoffka/Pictures/Иконки/dupes.png"))

    ret = msgBox.exec()


def display_detailed_error_message(message: str, ex: Exception):
    msgBox = QMessageBox()
    msgBox.setText("Ошибка.")
    msgBox.setInformativeText("Неизвестная ошибка")

    msgBox.setDetailedText(f"{type(ex)}: {str(ex)}")
    msgBox.setStandardButtons(QMessageBox.StandardButton.Close)
    ret = msgBox.exec()


def send_data(the_socket: socket.socket, raw_response: Any):
    response = pickle.dumps(raw_response)
    response_length = len(response)

    the_socket.send(struct.pack('>Q', response_length))
    the_socket.send(response)


def receive_data(the_socket: socket.socket):
    request_length = struct.unpack('>Q', the_socket.recv(8))[0]
    response = the_socket.recv(request_length)

    return pickle.loads(response)


def communicate_with_server(data: Any):
    result = (None, )

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 9999))
        client.settimeout(10000)

        send_data(client, data)

        result = receive_data(client)

        client.close()

    except Exception as e:
        print(e)

    return result


