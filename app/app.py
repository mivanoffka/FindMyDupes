import sys

from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication

app = QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon("/Users/mivanoffka/Pictures/Иконки/dupes.png"))


# app.setStyleSheet(content)
from main_window import MainWindow


window = MainWindow()
window.show()

app.exec()
