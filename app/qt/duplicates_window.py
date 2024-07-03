from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import *

from dupes.operations.duplicates_remover import DuplicatesRemover
from .progress_window import ProgressWindow
from .utility import MessageWindow
from .utility.enums import MessageResult
from .view_window import ViewWindow


class DuplicatesWindow(QDialog):
    __duplicates_groups_filtered: list
    __view_windows = []
    __names_and_full_names = {}
    __confirmation_window: MessageWindow = None

    def __init__(self, parent, result: list):
        super().__init__(parent=parent)

        self.__duplicates_groups_origin = result
        self.__duplicates_groups_filtered = self.__duplicates_groups_origin

        self.__init_ui()

    def __init_ui(self):
        #region Main widget and layout setup
        self.__main_widget = QWidget()
        self.__main_layout = QVBoxLayout()
        self.__main_layout.setSpacing(8)
        self.setLayout(self.__main_layout)
        #endregion

        #region Duplicates group box
        self.__duplicates_group_box = QGroupBox("Группы дубликатов")
        self.__main_layout.addWidget(self.__duplicates_group_box)

        self.__duplicates_group_box_layout = QVBoxLayout()
        self.__duplicates_group_box.setLayout(self.__duplicates_group_box_layout)
        self.__duplicates_tree_view = QTreeWidget()
        self.__duplicates_tree_view.itemDoubleClicked.connect(self.__on_dupicates_tree_view_double_clicked)
        self.__duplicates_group_box_layout.addWidget(self.__duplicates_tree_view)
        #endregion

        #region Full names checkbox
        self.__full_names_checkbox = QCheckBox("Полные имена файлов")
        self.__full_names_checkbox_layout = QHBoxLayout()
        self.__full_names_checkbox_layout.addWidget(self.__full_names_checkbox)
        self.__duplicates_group_box_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.__full_names_checkbox.checkStateChanged.connect(self.__refresh_tree_view)
        self.__duplicates_group_box_layout.addLayout(self.__full_names_checkbox_layout)
        self.__full_names_checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #endregion

        #region Duplicates tree view configuration
        self.__duplicates_tree_view.setColumnCount(1)
        self.__duplicates_tree_view.setHeaderLabel("Дважды нажмите на файл, чтобы открыть его")
        header = self.__duplicates_tree_view.header()
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)  # Пример выравнивания по центру

        #region Search text box
        self.__search_text_box = QLineEdit()
        self.__search_text_box.setPlaceholderText("Имя файла")
        #endregion

        #region Search group box
        self.__search_group_box = QGroupBox("Поиск группы по имени файла")
        self.__search_group_box.setFixedHeight(105)
        self.__main_layout.addWidget(self.__search_group_box)

        self.__search_group_box_layout = QVBoxLayout()
        self.__search_group_box.setLayout(self.__search_group_box_layout)

        self.__search_field_layout = QHBoxLayout()
        self.__search_group_box_layout.addLayout(self.__search_field_layout)
        self.__search_field_layout.addWidget(self.__search_text_box, 4)
        self.__search_group_box_layout.setSpacing(0)
        self.__search_field_layout.setSpacing(0)
        #endregion

        #region Search and reset buttons
        self.__search_button = QPushButton("Поиск")
        self.__reset_button = QPushButton("Сброс")

        self.__search_button.clicked.connect(self.__on_search_button_clicked)
        self.__reset_button.clicked.connect(self.__on_reset_button_clicked)

        self.__search_buttons_layout = QHBoxLayout()
        self.__search_buttons_layout.setSpacing(2)
        self.__search_group_box_layout.addLayout(self.__search_buttons_layout)
        self.__search_buttons_layout.addWidget(self.__search_button, 2)
        self.__search_buttons_layout.addWidget(self.__reset_button, 1)
        #endregion

        #region Actions buttons
        self.__remove_duplicates_button = QPushButton("Удалить дубликаты")
        self.__remove_duplicates_button.clicked.connect(self.__on_remove_button_clicked)
        self.__main_layout.addWidget(self.__remove_duplicates_button)
        #endregion

        # Устанавливаем цвет фона и текста заголовка через стили CSS
        header.setStyleSheet("""
            color: gray;
            font-size: 11px;
        """)
        #self.__duplicates_tree_view.setHeaderHidden(True)
        #endregion

        #region Refresh tree view
        self.__refresh_tree_view()
        #endregion

        #region Window title and size
        self.setWindowTitle("Результаты поиска")
        self.setFixedSize(350, 450)
        #endregion

    def __on_remove_button_clicked(self):
        message_result = MessageWindow.show_confirmation(
            "Вы уверены, что хотите удалить все дубликаты? Останется только один экземпляр из каждой группы.",
            title="Удаление дубликатов")
        if message_result == MessageResult.YES:
            task = DuplicatesRemover(self.__duplicates_groups_origin)
            self.__searching_window = ProgressWindow(self, task)
            self.__searching_window.finished.connect(self.__on_observable_task_finished)
            self.__searching_window.open()

    def __on_observable_task_finished(self):
        result = self.__searching_window.execution_result
        MessageWindow.show_task_result(result)
        self.__duplicates_groups_origin = result.value
        self.__refresh_tree_view()

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
        self.__names_and_full_names = {}
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
                self.__names_and_full_names[file.name] = str(file)
                p = str(file) if show_full_names else file.name
                item.setText(0, f"🌇 {p}")

        self.__duplicates_tree_view.expandAll()

    def __on_dupicates_tree_view_double_clicked(self, item: QTreeWidgetItem, column):
        if item.childCount() == 0:
            path = item.text(0)[2:] if self.__full_names_checkbox.isChecked() \
                                    else self.__names_and_full_names[item.text(0)[2:]]

            view_window = ViewWindow(self, path)
            view_window.show()


