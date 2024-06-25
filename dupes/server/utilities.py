import pickle
import socket
import struct
from typing import Any


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

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))
    client.settimeout(99999)

    send_data(client, data)

    result = receive_data(client)

    client.close()

    return result
