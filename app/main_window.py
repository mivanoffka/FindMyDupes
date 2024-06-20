from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *

from dupes import DupeFinder, DupeFinderByPhash
from dupes.image_folder import ALLOWED_FILE_FORMATS, ImageFolder
from searching_window import SearchingWindow


class MainWindow(QMainWindow):
    __folders_paths: list[str]

    def __init__(self):
        super().__init__()
        self.__folders_paths = []

        self.setWindowTitle("Find my dupes")
        self.setFixedSize(525, 275)

        self.__init_widgets()
        self.__init_folders_group_box()
        self.__init_formats_group_box()
        self.__connect_event_handlers()

        self.setCentralWidget(self.__main_widget)

        self.__main_layout.setSpacing(8)
        self.__main_widget.setLayout(self.__main_layout)
        self.__main_layout.addLayout(self.__group_boxes_layout)

        self.__search_button.setEnabled(False)
        self.__main_layout.addWidget(self.__search_button)

        self.__on_folders_list_item_changed()


    def __init_widgets(self):
        self.__main_widget = QWidget()
        self.__main_layout = QVBoxLayout()
        self.__group_boxes_layout = QHBoxLayout()

        self.__folders_group_box = QGroupBox("Папки с изображениями")
        self.__folders_group_box_layout = QVBoxLayout()

        self.__folders_list = QListWidget()
        self.__buttons_layout = QHBoxLayout()

        self.__add_button = QPushButton("Добавить")
        self.__remove_button = QPushButton("Удалить")

        self.__formats_group_box = QGroupBox("Типы")
        self.__formats_check_boxes = {}
        self.__search_button = QPushButton("Поиск дубликатов")

    def __init_folders_group_box(self):
        self.__folders_group_box_layout.setSpacing(2)
        self.__folders_group_box.setLayout(self.__folders_group_box_layout)
        self.__group_boxes_layout.addWidget(self.__folders_group_box, 2)

        self.__folders_list.setSpacing(2)
        self.__folders_group_box_layout.addWidget(self.__folders_list)

        self.__buttons_layout.setSpacing(6)
        self.__remove_button.setEnabled(False)

        self.__buttons_layout.addWidget(self.__add_button, 3)
        self.__buttons_layout.addWidget(self.__remove_button, 2)
        self.__folders_group_box_layout.addLayout(self.__buttons_layout)

    def __init_formats_group_box(self):
        self.__formats_group_box.setFixedWidth(100)
        formats_group_layout = QVBoxLayout()
        formats_group_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        formats_group_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        formats_group_layout.setSpacing(12)

        self.__formats_group_box.setLayout(formats_group_layout)
        self.__group_boxes_layout.addWidget(self.__formats_group_box, 1)

        for file_format in ALLOWED_FILE_FORMATS:
            self.__formats_check_boxes[file_format] = QCheckBox(file_format)
            self.__formats_check_boxes[file_format].setChecked(True)
            formats_group_layout.addWidget(self.__formats_check_boxes[file_format])

    def __connect_event_handlers(self):
        self.__add_button.clicked.connect(self.__on_add_button_click)
        self.__remove_button.clicked.connect(self.__on_remove_button_click)
        self.__folders_list.itemSelectionChanged.connect(self.__on_folders_list_item_changed)
        self.__search_button.clicked.connect(self.__on_search_button_clicked)

    def __on_add_button_click(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Выберите папку')
        if folder_path:
            if folder_path not in self.__folders_paths:
                self.__folders_paths.append(folder_path)

        self.update_folders_list()

    def __on_remove_button_click(self):
        if len(self.__folders_list.selectedItems()) > 0:
            self.__folders_paths.remove(self.__folders_list.selectedItems()[0].text())
        self.update_folders_list()

    def __on_search_button_clicked(self):
        image_folders = []
        for path in self.__folders_paths:
            image_folders.append(ImageFolder(path))

        finder = DupeFinderByPhash(*image_folders)

        self.__searching_window = SearchingWindow(finder)
        self.__searching_window.show()

    def __get_formats_filter(self):
        return (key for key, value in self.__formats_check_boxes.items() if value.isChecked())

    def __on_folders_list_item_changed(self):
        self.__remove_button.setEnabled(len(self.__folders_list.selectedItems()) > 0)
        self.__search_button.setEnabled(len(self.__folders_paths) > 0)

    def update_folders_list(self):
        self.__folders_list.clear()
        self.__folders_list.addItems(self.__folders_paths)
        self.__on_folders_list_item_changed()




