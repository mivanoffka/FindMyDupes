import threading
from typing import Optional

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *

from dupes import DupeFinder
import time


class SearchingWindow(QWidget):
    __dupe_finder: DupeFinder
    __finding_result: Optional[list] = None

    def __init_widgets(self):
        self.__main_layout = QVBoxLayout()
        self.__progress_bar = QProgressBar()
        self.__progress_bar.setRange(0, 100)
        self.__percentage_label = QLabel("0%")

    def __init__(self, dupe_finder: DupeFinder):
        super().__init__()

        self.__dupe_finder = dupe_finder

        self.__init_widgets()

        self.__main_layout.setSpacing(8)
        self.setLayout(self.__main_layout)
        self.__main_layout.addWidget(self.__progress_bar)
        self.__main_layout.addWidget(self.__percentage_label)
        self.__percentage_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.setWindowTitle("Выполняется поиск...")
        self.setFixedSize(400, 75)

        self.__launch_finder()

    def __launch_finder(self):
        threading.Thread(target=self.__progress_thread).start()
        threading.Thread(target=self.__searching_thread).start()

    def __progress_thread(self):
        while self.__finding_result is None:
            percentage = round(self.__dupe_finder.progress * 100, 1)
            self.__percentage_label.setText(f"{percentage}%")
            self.__progress_bar.setValue(int(percentage))
            time.sleep(0.1)

        percentage = round(self.__dupe_finder.progress * 100, 1)
        self.__percentage_label.setText(f"{percentage}%")
        self.__progress_bar.setValue(int(percentage))

    def __searching_thread(self):
        self.__finding_result = self.__dupe_finder.start_searching()

        # count = len(self.__finding_result)
        # msgBox = QMessageBox()
        # msgBox.setIcon(QMessageBox.Icon.Warning)
        # msgBox.setText(f"Найдено {count} групп дубликатов.")
        # msgBox.setWindowTitle("Готово!")
        # msgBox.exec()

