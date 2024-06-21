from PyQt6.QtWidgets import QMessageBox

import sys
import traceback


def display_message(message: str, title="Сообщение"):
    msgBox = QMessageBox()
    msgBox.setText(title)
    msgBox.setInformativeText(message)
    msgBox.setStandardButtons(QMessageBox.StandardButton.Close)
    ret = msgBox.exec()


def display_detailed_error_message(message: str, ex: Exception):
    msgBox = QMessageBox()
    msgBox.setText("Ошибка.")
    msgBox.setInformativeText("Неизвестная ошибка")

    msgBox.setDetailedText(f"{type(ex)}: {str(ex)}")
    msgBox.setStandardButtons(QMessageBox.StandardButton.Close)
    ret = msgBox.exec()

