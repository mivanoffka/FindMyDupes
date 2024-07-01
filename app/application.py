import ctypes
import platform
import subprocess
import sys
import threading

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from config import BASE_DIR
from dupes import InternalServerManager
from logger import Logger
from .qt.main_window import MainWindow
from .qt.utility import display_detailed_error_message

import logging


class Application:
    __app: QApplication
    __internal_server_process: subprocess.Popen
    __main_window: MainWindow
    __logger: Logger

    def rerun_as_admin(self):
        match platform.system():
            case "Windows":
                if not ctypes.windll.shell32.IsUserAnAdmin():
                    ctypes.windll.shell32.ShellExecuteW(
                        None, "runas", sys.executable, f'{BASE_DIR / "main.py"}', None, 1)
                    sys.exit(0)
                else:
                    return

            case "Darwin" | "Linux":
                return

    def set_stylesheet(self):
        if platform.system() == "Windows":
            with open(str(BASE_DIR / "app/assets/style.qss")) as f:
                self.__app.setStyleSheet(f.read())

    def finish(self):
        InternalServerManager().communicate_with("TERMINATE", dont_wait_for_response=True)

    def start(self):
        self.rerun_as_admin()

        self.__app = QApplication(sys.argv)

        self.__logger = Logger("app/logs/client")
        self.__logger.setup()

        try:
            port = InternalServerManager().launch()
            if port is not None:
                logging.info("Internal server started at " + str(port))
            else:
                from dupes.exceptions import ServerNotStartedError
                raise ServerNotStartedError("No information can be provided here. Go to server logs.")
        except Exception as error:
            logging.error("Failed to start internal server: " + str(error))
            display_detailed_error_message(error, "Приложение не удалось запустить"
                                                  " из-за проблемы с запуском внутреннего сервера.", )
            self.finish()
            return

        try:
            self.__app.setWindowIcon(QIcon(str(BASE_DIR / "assets/icon.png")))
            self.set_stylesheet()
            self.__main_window = MainWindow()
            self.__main_window.show()
            self.__app.exec()
        except Exception as error:
            display_detailed_error_message(error, "Произошла критическая ошибка!", )

        self.finish()

