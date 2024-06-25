import subprocess
import sys

from PyQt6.QtWidgets import QApplication

from dupes import InternalServer
from qt.main_window import MainWindow
from qt.utility import display_detailed_error_message


class Application:
    __app: QApplication
    __main_window: MainWindow
    __internal_server_process: subprocess.Popen

    def __init__(self):
        self.__app = QApplication(sys.argv)
        self.__main_window = MainWindow()

    def start(self):
        try:
            InternalServer().launch_process()
        except Exception as error:
            display_detailed_error_message(error, "Приложение не удалось запустить"
                                                  " из-за проблемы с запуском внутреннего сервера.", )
            return
        try:
            self.__main_window.show()
            self.__app.exec()
        except Exception as error:
            display_detailed_error_message(error, "Произошла критическая ошибка!", )

        InternalServer().communicate_with("TERMINATE")


if __name__ == "__main__":
    app = Application()
    app.start()
