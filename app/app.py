import subprocess
import sys
import time

from PyQt6.QtWidgets import QApplication

from qt.main_window import MainWindow
from dupes.server import communicate_with_server


class Application:
    __app: QApplication
    __main_window: MainWindow
    __internal_server_process: subprocess.Popen

    def __init__(self):
        self.__app = QApplication(sys.argv)
        self.__main_window = MainWindow()

    def start(self):
        try:
            self.__internal_server_process = subprocess.Popen(["python", "server_script.py"])
            time.sleep(2)
            if not communicate_with_server("IS_ALIVE"):
                raise Exception()

        except Exception as error:
            print("Unable to start internal server process.\n " + str(error))
            return

        print("Internal server process started.")

        try:
            self.__main_window.show()
            self.__app.exec()
        except Exception as error:
            print("A critical error has occurred.\n " + str(error))

        try:
            communicate_with_server("TERMINATE")
            print("Internal server process terminated.")
        except Exception as error:
            print("Unable to terminate internal server process.\n " + str(error))


if __name__ == "__main__":
    app = Application()
    app.start()
