from pathlib import Path
from typing import Optional, Any

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import *

from PySide6.QtCore import QThread

from .utility import ProgressDisplay
from dupes import ObservableTask

from .utility import ObservableTaskWorker


class DuplicatesWindow(QDialog):
    __duplicates_groups_filtered: list

    def __init__(self, parent, result: list):
        super().__init__(parent=parent)

        self.__duplicates_groups_origin = result
        self.__duplicates_groups_filtered = self.__duplicates_groups_origin

        self.__main_widget = QWidget()
        self.__main_layout = QVBoxLayout()
        self.__main_layout.setSpacing(8)
        self.setLayout(self.__main_layout)

        self.__search_text_box = QLineEdit()
        self.__search_text_box.setPlaceholderText("Имя файла")

        self.__duplicates_group_box = QGroupBox("Группы дубликатов")
        self.__main_layout.addWidget(self.__duplicates_group_box)

        self.__duplicates_group_box_layout = QVBoxLayout()
        self.__duplicates_group_box.setLayout(self.__duplicates_group_box_layout)

        self.__duplicates_tree_view = QTreeWidget()
        self.__duplicates_group_box_layout.addWidget(self.__duplicates_tree_view)

        self.__full_names_checkbox = QCheckBox("Полные имена файлов")
        self.__full_names_checkbox_layout = QHBoxLayout()
        self.__full_names_checkbox_layout.addWidget(self.__full_names_checkbox)
        self.__duplicates_group_box_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.__full_names_checkbox.checkStateChanged.connect(self.__refresh_tree_view)
        self.__duplicates_group_box_layout.addLayout(self.__full_names_checkbox_layout)
        self.__full_names_checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.__search_group_box = QGroupBox("Поиск группы по имени файла")
        self.__search_group_box.setFixedHeight(105)
        self.__main_layout.addWidget(self.__search_group_box)

        self.__search_button = QPushButton("Поиск")
        self.__reset_button = QPushButton("Сброс")

        self.__search_button.clicked.connect(self.__on_search_button_clicked)
        self.__reset_button.clicked.connect(self.__on_reset_button_clicked)

        self.__search_group_box_layout = QVBoxLayout()
        self.__search_group_box.setLayout(self.__search_group_box_layout)

        self.__search_field_layout = QHBoxLayout()
        self.__search_group_box_layout.addLayout(self.__search_field_layout)
        self.__search_field_layout.addWidget(self.__search_text_box, 4)
        self.__search_group_box_layout.setSpacing(0)
        self.__search_field_layout.setSpacing(0)

        self.__search_buttons_layout = QHBoxLayout()
        self.__search_buttons_layout.setSpacing(2)
        self.__search_group_box_layout.addLayout(self.__search_buttons_layout)
        self.__search_buttons_layout.addWidget(self.__search_button, 2)
        self.__search_buttons_layout.addWidget(self.__reset_button, 1)

        self.__duplicates_tree_view.setColumnCount(1)
        self.__duplicates_tree_view.setHeaderHidden(True)

        self.__refresh_tree_view()
        self.setWindowTitle("Результаты поиска")
        self.setFixedSize(350, 450)

    def __on_reset_button_clicked(self):
        self.__search_text_box.setText("")
        self.__duplicates_groups_filtered = self.__duplicates_groups_origin
        self.__refresh_tree_view()

    def __on_search_button_clicked(self):
        query_text = self.__search_text_box.text()
        filtered_groups = []
        for group in self.__duplicates_groups_origin:
            for path in group:
                if query_text in str(path):
                    filtered_groups.append(group)
                    break
        self.__duplicates_groups_filtered = filtered_groups
        self.__refresh_tree_view()

    def __refresh_tree_view(self):
        show_full_names = self.__full_names_checkbox.isChecked()

        self.__duplicates_tree_view.clear()
        self.setFixedSize(600 if show_full_names else 350, 450)
        for i, group in enumerate(self.__duplicates_groups_filtered):
            tree_group = QTreeWidgetItem(self.__duplicates_tree_view)
            tree_group.setText(0, f"Группа {i+1}")
            tree_group.setForeground(0, QBrush(QColor("gray")))
            for file in group:
                file: Path = file
                item = QTreeWidgetItem(tree_group)
                item.setText(0, str(file) if show_full_names else file.name)

        self.__duplicates_tree_view.expandAll()



