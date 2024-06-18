import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Find my dupes")
        self.setFixedSize(QSize(600, 400))

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(8)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        group_boxes_layout = QHBoxLayout()
        main_layout.addLayout(group_boxes_layout)

        folders_group = QGroupBox("Папки с изображениями")
        folders_group_layout = QVBoxLayout()
        folders_group_layout.setSpacing(2)
        folders_group.setLayout(folders_group_layout)
        group_boxes_layout.addWidget(folders_group, 3)

        folders_list = QListWidget()
        folders_group_layout.addWidget(folders_list)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(6)
        add_button = QPushButton("Добавить")
        remove_button = QPushButton("Удалить")
        buttons_layout.addWidget(add_button, 2)
        buttons_layout.addWidget(remove_button)
        folders_group_layout.addLayout(buttons_layout)

        formats_group = QGroupBox("Форматы файлов")
        formats_group_layout = QVBoxLayout()
        formats_group.setLayout(formats_group_layout)
        group_boxes_layout.addWidget(formats_group, 1)

        search_button = QPushButton("Поиск дубликатов")
        main_layout.addWidget(search_button)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
