from PyQt6.QtWidgets import QMessageBox
import traceback


def display_message(message: str, title="Сообщение", action_on_closed=None):
    msgBox = QMessageBox()
    msgBox.setText(title)
    msgBox.setInformativeText(message)
    msgBox.finished.connect(action_on_closed)
    msgBox.setStandardButtons(QMessageBox.StandardButton.Close)

    ret = msgBox.exec()


def display_detailed_error_message(ex: Exception, message="Неизвестная ошибка."):
    msgBox = QMessageBox()
    msgBox.setText("Ошибка.")
    msgBox.setInformativeText(f"{message}")
    detailed_text = traceback.format_exc()

    msgBox.setDetailedText(f"{type(ex)}: {str(ex)}\n\n{detailed_text}")
    ret = msgBox.exec()
