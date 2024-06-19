import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *


class MainWindow(QMainWindow):
    folders_paths: list[str] = []

    def __init__(self):
        super().__init__()
        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle("Find my dupes")
        self.setFixedSize(525, 275)

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
        group_boxes_layout.addWidget(folders_group, 2)

        self.folders_list = QListWidget()
        self.folders_list.setSpacing(2)
        self.folders_list.itemSelectionChanged.connect(self.on_folders_list_item_changed)
        folders_group_layout.addWidget(self.folders_list)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(6)
        add_button = QPushButton("Добавить")
        add_button.clicked.connect(self.on_add_button_click)

        self.remove_button = QPushButton("Удалить")
        self.remove_button.clicked.connect(self.on_delete_button_click)
        self.remove_button.setEnabled(False)

        buttons_layout.addWidget(add_button, 2)
        buttons_layout.addWidget(self.remove_button)
        folders_group_layout.addLayout(buttons_layout)

        formats_group = QGroupBox("Типы")
        formats_group.setFixedWidth(100)
        formats_group_layout = QVBoxLayout()
        formats_group_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        formats_group_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        formats_group_layout.setSpacing(12)

        formats_group.setLayout(formats_group_layout)
        group_boxes_layout.addWidget(formats_group, 1)

        formats = (" .JPEG", " .PNG", " .BMP", " .GIF", " .TIFF", " .WEBP", " .ICO")
        for format in formats:
            format_check_box = QCheckBox(format)
            format_check_box.setChecked(True)
            formats_group_layout.addWidget(format_check_box)

        self.search_button = QPushButton("Поиск дубликатов")
        self.search_button.setEnabled(False)
        self.search_button.clicked.connect(self.on_search_button_clicked)
        main_layout.addWidget(self.search_button)

    def on_add_button_click(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Выберите папку')
        if folder_path:
            if folder_path not in self.folders_paths:
                self.folders_paths.append(folder_path)

        self.update_folders_list()

    def on_delete_button_click(self):
        if len(self.folders_list.selectedItems()) > 0:
            self.folders_paths.remove(self.folders_list.selectedItems()[0].text())
        self.update_folders_list()

    def on_folders_list_item_changed(self):
        self.remove_button.setEnabled(len(self.folders_list.selectedItems()) > 0)
        self.search_button.setEnabled(len(self.folders_paths) > 0)

    def on_search_button_clicked(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Icon.Warning)
        msgBox.setText("Когда-нибудь эта кнопка будет что-то делать")
        msgBox.setWindowTitle("Упс...")
        msgBox.exec()
        #msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    def update_folders_list(self):
        self.folders_list.clear()
        self.folders_list.addItems(self.folders_paths)
        self.on_folders_list_item_changed()


# Откройте файл в режиме чтения ('r')
# with open('/Users/mivanoffka/Desktop/style.qss', 'r') as file:
#     content = file.read()

# Теперь переменная content содержит данные файла в виде строки

app = QApplication(sys.argv)

# app.setStyleSheet(content)

window = MainWindow()
window.show()

app.exec()
