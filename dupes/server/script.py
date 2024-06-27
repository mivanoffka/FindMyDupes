import sys
from dupes import Server


if __name__ == '__main__':
    port = int(sys.argv[1])
    server = Server(port=port)
    server.launch()

