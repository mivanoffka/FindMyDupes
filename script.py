import sys
from server import InternalServer


if __name__ == '__main__':
    port = int(sys.argv[1])
    server = InternalServer(port=port)
    server.launch()

