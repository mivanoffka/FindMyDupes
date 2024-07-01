from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import *

from dupes import ObservableTask
from .utility import ProgressDisplayingWindow, MessageWindow


class ViewWindow(QDialog):
    def __init__(self, parent, image_path: str):
        super().__init__(parent=parent)
        self.__main_widget = QWidget()
        self.__main_widget.setContentsMargins(0, 0, 0, 0)
        self.__main_layout = QVBoxLayout()
        self.__main_layout.setSpacing(0)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.__main_layout)

        self.label = QLabel(self)
        self.label.setMargin(0)
        self.label.setContentsMargins(0, 0, 0, 0)
        pixmap = QPixmap(image_path)

        self.__main_layout.addWidget(self.label)

        if pixmap.isNull():
            MessageWindow.display_error("Не удалось открыть изображение")
            self.close()

        max_dimension = 600
        min_dimension = 200
        original_width = pixmap.width()
        original_height = pixmap.height()

        scale = min(max_dimension / max(original_width, original_height),
                    max(original_width, original_height) / min_dimension)

        # Calculate new dimensions
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)

        # Resize the pixmap
        self.pixmap = pixmap.scaled(new_width, new_height, mode=Qt.TransformationMode.SmoothTransformation)

        # Устанавливаем QPixmap в QLabel
        self.label.setPixmap(self.pixmap)
        self.setFixedSize(new_width, new_height)
        self.setWindowTitle(Path(image_path).name)
