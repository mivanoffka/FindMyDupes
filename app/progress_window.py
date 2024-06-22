import threading
from typing import Optional, Any

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *

from PySide6.QtCore import Signal, QThread, QObject

from .progressdisplay import ProgressDisplay
from .utilities import display_message, display_detailed_error_message
from dupes import DupeFinder, ObservableTask
from dupes.exceptions import NoValidImagesError, EmptyFoldersError
import time

from .background_task import ObservableTaskWorker


class ProgressWindow(QDialog, ProgressDisplay):
    __task: ObservableTask
    __finding_result: Optional[list] = None
    __execution_result: Any = None

    @property
    def execution_result(self) -> Any:
        return self.__execution_result

    @property
    def task_thread(self) -> QThread:
        return self.__task_thread

    @property
    def progress_thread(self) -> QThread:
        return self.__progress_thread

    def on_task_finish(self, result: Any):
        self.__execution_result = result
        self.close()

    def __init__(self, parent, task: ObservableTask):
        super().__init__(parent=parent)

        self.__task = task

        self.__main_widget = QWidget()
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

        self.__setup()

    def __setup(self):
        self.__task_thread = QThread()
        self.__progress_thread = QThread()

        task_worker = ObservableTaskWorker(self.__task, self)
        task_worker.start()

    def update_progress(self, percentage):
        self.__percentage_label.setText(f"{percentage}%")
        self.__progress_bar.setValue(int(percentage))

    def display_result(self, result):
        count = result[0]
        duration = round(result[1].total_seconds() / 1000, 1)

        self.__percentage_label.setText(f"Найдено {count} групп(ы) дубликатов за {duration} c.")
        self.__progress_bar.setValue(100)


