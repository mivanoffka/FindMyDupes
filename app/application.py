import ctypes
import subprocess
import sys
import platform
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from .qt.main_window import MainWindow
from .qt.utility import display_detailed_error_message

from dupes import InternalServer

from config import BASE_DIR


class Application:
    __app: QApplication
    __internal_server_process: subprocess.Popen
    __main_window: MainWindow

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

    def start(self):
        self.rerun_as_admin()
        self.__app = QApplication(sys.argv)
        try:
            InternalServer().launch_process()
        except Exception as error:
            display_detailed_error_message(error, "Приложение не удалось запустить"
                                                  " из-за проблемы с запуском внутреннего сервера.", )
            return
        try:
            self.__app.setWindowIcon(QIcon(str(BASE_DIR / "assets/icon.png")))
            self.set_stylesheet()
            self.__main_window = MainWindow()
            self.__main_window.show()
            self.__app.exec()
        except Exception as error:
            display_detailed_error_message(error, "Произошла критическая ошибка!", )

        InternalServer().communicate_with("TERMINATE")
