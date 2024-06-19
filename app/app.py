import sys

from PyQt6.QtWidgets import QApplication

app = QApplication(sys.argv)

# app.setStyleSheet(content)
from main_window import MainWindow



window = MainWindow()
window.show()

app.exec()
