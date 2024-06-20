import threading
from typing import Optional

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *

from PySide6.QtCore import Signal, QThread, QObject

from utilities import display_error_message, display_detailed_error_message
from dupes import DupeFinder, NoValidImagesError, EmptyFoldersError
import time


class SearchWorker(QObject):
    finished = Signal()
    failed = Signal(str)
    failed_unknown = Signal(str, Exception)
    result = None

    def __init__(self, finder: DupeFinder):
        super().__init__()
        self.finder = finder

    def run(self):
        try:
            self.result = self.finder.search()
        except NoValidImagesError as error:
            self.failed.emit("Ни один файл не удалось открыть и/или обработать")
        except Exception as error:
            self.failed_unknown.emit("Неизвестная ошибка", error)

        self.finished.emit()


class ProgressWorker(QObject):
    progress = Signal(float)
    finished = Signal(int)

    def __init__(self, search_worker: SearchWorker):
        super().__init__()
        self.search_worker = search_worker

    def run(self):
        while self.search_worker.result is None:
            percentage = round(self.search_worker.finder.progress * 100, 1)
            self.progress.emit(percentage)
            time.sleep(0.1)

        self.finished.emit(len(self.search_worker.result))


class SearchingWindow(QWidget):
    __dupe_finder: DupeFinder
    __finding_result: Optional[list] = None

    def __init__(self, dupe_finder: DupeFinder):
        super().__init__()

        self.__dupe_finder = dupe_finder

        self.__main_layout = QVBoxLayout()
        self.__main_layout.setSpacing(8)
        self.setLayout(self.__main_layout)

        self.__progress_bar = QProgressBar()
        self.__progress_bar.setRange(0, 100)
        self.__percentage_label = QLabel("0%")
        self.__percentage_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.__main_layout.addWidget(self.__progress_bar)
        self.__main_layout.addWidget(self.__percentage_label)

        self.setWindowTitle("Выполняется поиск...")
        self.setFixedSize(400, 75)

        self.__launch_finder()

    def __launch_finder(self):
        self.search_thread = QThread()
        self.search_worker = SearchWorker(self.__dupe_finder)
        self.search_worker.moveToThread(self.search_thread)

        self.search_thread.started.connect(self.search_worker.run)
        self.search_worker.finished.connect(self.search_thread.quit)
        self.search_worker.finished.connect(self.search_worker.deleteLater)
        self.search_thread.finished.connect(self.search_thread.deleteLater)
        self.search_worker.failed.connect(display_error_message)
        self.search_worker.failed_unknown.connect(display_detailed_error_message)



        self.progress_thread = QThread()
        self.progress_worker = ProgressWorker(self.search_worker)
        self.progress_worker.moveToThread(self.progress_thread)

        self.progress_thread.started.connect(self.progress_worker.run)
        self.progress_worker.finished.connect(self.progress_thread.quit)
        self.progress_worker.finished.connect(self.progress_worker.deleteLater)
        self.progress_thread.finished.connect(self.progress_thread.deleteLater)
        self.progress_worker.progress.connect(self.update_progress)
        #self.progress_worker.finished.connect(lambda: self.update_progress(100))
        self.progress_worker.finished.connect(self.display_result)

        self.search_thread.start()
        self.progress_thread.start()


    def update_progress(self, percentage):
        self.__percentage_label.setText(f"{percentage}%")
        self.__progress_bar.setValue(int(percentage))

    def display_result(self, result):
        self.__percentage_label.setText(f"Найдено {result} групп дубликатов")
        self.__progress_bar.setValue(100)
