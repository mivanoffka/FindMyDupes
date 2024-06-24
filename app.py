import subprocess
import sys
from PyQt6.QtWidgets import QApplication

from app.main_window import MainWindow

server_process: subprocess.Popen = subprocess.Popen(["python", "server.py"])

try:
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
except Exception as error:
    print(error)

server_process.terminate()


