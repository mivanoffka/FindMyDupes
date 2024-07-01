from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import *

from dupes import ObservableTask


class MessageWindow(QDialog):
    windows_container = []

    def __init__(self, message, title="Сообщение", icon_emoji: str = "ℹ️", action_on_closed=None):
        super().__init__()

        MessageWindow.windows_container.append(self)

        self.__main_widget = QWidget()
        self.__main_widget.setContentsMargins(0, 0, 0, 0)
        self.__main_layout = QVBoxLayout()
        self.__main_layout.setSpacing(12)
        self.__main_widget.setLayout(self.__main_layout)
        self.setLayout(self.__main_layout)

        self.__icon_and_message_layout = QHBoxLayout()
        self.__main_layout.addLayout(self.__icon_and_message_layout)

        self.__icon_label = QLabel(icon_emoji)
        self.__icon_label.setStyleSheet("font-size: 48px;")
        self.__icon_and_message_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.__icon_and_message_layout.addWidget(self.__icon_label, 1)

        self.__message_label = QLabel(message)
        self.__message_label.setWordWrap(True)
        self.__icon_and_message_layout.addWidget(self.__message_label, 6)

        self.__ok_button = QPushButton("OK")
        self.__ok_button.clicked.connect(self.on_ok_button_clicked)
        self.__main_layout.addWidget(self.__ok_button)

        height_delta = 27
        line_len = 32
        height = height_delta * len(message) // line_len
        self.__message_label.setFixedHeight(height)
        self.setFixedWidth(320)
        self.setWindowTitle(title)

        self.finished.connect(action_on_closed)

    def on_ok_button_clicked(self):
        self.close()

    @staticmethod
    def display_modal(message, title="Сообщение", icon_emoji="ℹ️", action_on_closed=None):
        message_window = MessageWindow(message, title, icon_emoji, action_on_closed)
        message_window.exec()

    @staticmethod
    def display(message, title="Сообщение", icon_emoji="ℹ️", action_on_closed=None):
        message_window = MessageWindow(message, title, icon_emoji, action_on_closed)
        message_window.show()

    @staticmethod
    def display_error(message):
        message_window = MessageWindow(message, title="Ошибка", icon_emoji="❌")
        message_window.show()

