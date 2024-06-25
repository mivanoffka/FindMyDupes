import platform
import getpass

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *

from dupes import DupeFinderByHash, DupeFinderByHashMultiThread
from dupes.exceptions import *
from dupes.utility.image_folder import ALLOWED_FILE_FORMATS, ImageFolder

from .utility import display_message, ProgressDisplay
from .progress_window import ProgressWindow


class MainWindow(QMainWindow):
    __folders_paths: list[str]
    __os = platform.system()
    __username = getpass.getuser()

    DEFAULT_PICTURES_PATHS = {
        "Darwin": "Users/{}/Pictures"
    }

    @property
    def default_pictures_path(self):
        return self.DEFAULT_PICTURES_PATHS[self.__os].format(self.__username)


    def __init__(self):
        super().__init__()
        self.__folders_paths = []

        self.setWindowTitle("Find my dupes")
        self.setFixedSize(525, 325)

        self.__init_widgets()
        self.__init_folders_group_box()
        self.__init_formats_group_box()
        self.__connect_event_handlers()

        self.setCentralWidget(self.__main_widget)

        self.__main_layout.setSpacing(8)
        self.__main_widget.setLayout(self.__main_layout)
        self.__main_layout.addLayout(self.__group_boxes_layout)

        self.__options_group_boxes_layout = QHBoxLayout()
        self.__main_layout.addLayout(self.__options_group_boxes_layout)

        self.__method_group_box = QGroupBox("Метод поиска")
        self.__options_group_boxes_layout.addWidget(self.__method_group_box, 2)
        self.__options_group_boxes_layout.setSpacing(8)
        self.__method_group_box_layout = QVBoxLayout()
        self.__method_group_box.setLayout(self.__method_group_box_layout)
        self.__method_combo_box = QComboBox()
        self.__method_combo_box.addItem("Хеширование")
        self.__method_combo_box.addItem("Хеширование (однопоточн.)")


        #self.__method_combo_box.addItem("Нейросеть")
        self.__method_group_box_layout.addWidget(self.__method_combo_box)

        self.__precision_group_box = QGroupBox("Процент схожести изображений")
        self.__options_group_boxes_layout.addWidget(self.__precision_group_box, 3)
        self.__precision_group_box_layout = QHBoxLayout()
        self.__precision_group_box_layout.setSpacing(12)
        self.__precision_group_box.setLayout(self.__precision_group_box_layout)
        self.__precision_label = QLabel("90%")
        self.__precision_group_box_layout.addWidget(self.__precision_label)

        self.__precision_slider = QSlider(Qt.Orientation.Horizontal)
        self.__precision_slider.setMinimum(0)
        self.__precision_slider.setMaximum(100)
        self.__precision_slider.setValue(90)
        self.__precision_slider.valueChanged.connect(
            lambda: self.__precision_label.setText(f"{self.__precision_slider.value()}%")
        )
        self.__precision_group_box_layout.addWidget(self.__precision_slider)
        # self.__help_button = QPushButton("?")
        # self.__precision_group_box_layout.addWidget(self.__help_button)

        self.__search_button.setEnabled(False)
        self.__main_layout.addWidget(self.__search_button)

        self.__on_folders_list_item_changed()

    def __init_widgets(self):
        self.__main_widget = QWidget()
        self.__main_layout = QVBoxLayout()
        self.__group_boxes_layout = QHBoxLayout()
        self.__group_boxes_layout.setSpacing(8)

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
        try:
            formats_filter = self.__get_formats_filter()

            image_folders = []
            for path in self.__folders_paths:
                image_folders.append(ImageFolder(path, formats_filter))

            precision = self.__precision_slider.value() / 100

            finder_types = {1: DupeFinderByHash, 0: DupeFinderByHashMultiThread}

            finder_type = finder_types[self.__method_combo_box.currentIndex()]

            finder = finder_type(*image_folders, precision=precision)

            self.__searching_window = ProgressWindow(self, finder)
            self.__searching_window.finished.connect(self.__on_search_finished)
            self.__searching_window.open()

        except EmptyFoldersError as error:
            display_message("В указанных папках не удалось найти ни одного файла,"
                                  " который бы соответствовал выбранным форматам."
                                  " \r\n\r\nЧтобы осуществить поиск дубликатов, файлов должно быть хотя бы два.")
        except NoFormatsProvided as error:
            display_message("Пожалуйста, выберите хотя бы один тип файла.")

    def __on_search_finished(self):
        result = self.__searching_window.execution_result
        if result is not None:

            count = len(result[0])
            duration = round(result[1].total_seconds(), 1)

            message = f"Найдено {count} групп(ы) дубликатов.\r\n\r\n Поиск занял {duration} c. "\
                if len(result) > 0 else f"Дубликатов не найдено.\r\n\r\n Поиск занял {duration} c. "
            title = "Поиск завершён!"
            display_message(message, title)

    def __get_formats_filter(self):
        formats = [key for key, value in self.__formats_check_boxes.items() if value.isChecked()]
        if len(formats) > 0:
            return formats
        else:
            raise NoFormatsProvided("Please select at least one file format")

    def __on_folders_list_item_changed(self):
        self.__remove_button.setEnabled(len(self.__folders_list.selectedItems()) > 0)
        self.__search_button.setEnabled(len(self.__folders_paths) > 0)

    def update_folders_list(self):
        self.__folders_list.clear()
        self.__folders_list.addItems(self.__folders_paths)
        self.__on_folders_list_item_changed()




