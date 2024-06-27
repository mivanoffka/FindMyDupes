import subprocess
import sys
import platform

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from dupes import InternalServer
from qt.main_window import MainWindow
from qt.utility import display_detailed_error_message

from config import BASE_DIR


class Application:
    __app: QApplication
    __main_window: MainWindow
    __internal_server_process: subprocess.Popen

    def set_stylesheet(self):
        if platform.system() == "Windows":
            with open(str(BASE_DIR / "app/assets/style.qss")) as f:
                self.__app.setStyleSheet(f.read())
        ...

    def start(self):
        try:
            InternalServer().launch_process()
        except Exception as error:
            display_detailed_error_message(error, "Приложение не удалось запустить"
                                                  " из-за проблемы с запуском внутреннего сервера.", )
            return
        try:
            self.__app = QApplication(sys.argv)
            self.__app.setWindowIcon(QIcon(str(BASE_DIR / "assets/dupes.png")))
            self.set_stylesheet()
            self.__main_window = MainWindow()
            self.__main_window.show()
            self.__app.exec()
        except Exception as error:
            display_detailed_error_message(error, "Произошла критическая ошибка!", )


if __name__ == "__main__":
    app = Application()
    app.start()
