from abc import abstractmethod
import time
from typing import Any

from dupes import DupeFinder, ObservableTask
from .utilities import display_message

from PySide6.QtCore import Signal, QObject, QThread
from .progressable import Progressable


class BackgroundTaskWorkerDefinition(QObject):
    finished: Signal = Signal()
    result = None

    @abstractmethod
    def execute(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def progress(self) -> float:
        raise NotImplementedError()

    def run(self):
        try:
            self.result = self.execute()
        except Exception as error:
            display_message(str(error))

        self.finished.emit()


class ProgressWorker(QObject):
    bg_worker: BackgroundTaskWorkerDefinition
    progress = Signal(float)
    finished = Signal(object)

    def __init__(self, bg_worker: BackgroundTaskWorkerDefinition):
        super().__init__()
        self.bg_worker = bg_worker

    def run(self):
        while self.bg_worker.result is None:
            percentage = round(self.bg_worker.progress * 100, 1)
            self.progress.emit(percentage)
            time.sleep(0.1)

        self.progress.emit(100)
        time.sleep(0.1)
        self.finished.emit(self.bg_worker.result)


class BackgroundTaskWorker(BackgroundTaskWorkerDefinition):
    progress_worker: ProgressWorker

    @abstractmethod
    def execute(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def progress(self) -> float:
        raise NotImplementedError()

    def __init__(self, progressable: Progressable):
        bg_task_thread = progressable.task_thread
        progress_thread = progressable.progress_thread
        gui_progress_updater = progressable.update_progress
        on_finish = progressable.on_task_finish

        self.bg_task_thread = bg_task_thread
        self.progress_thread = progress_thread

        super().__init__()
        self.moveToThread(bg_task_thread)

        self.finished.connect(bg_task_thread.quit)
        self.finished.connect(self.deleteLater)

        bg_task_thread.started.connect(self.run)
        bg_task_thread.finished.connect(bg_task_thread.deleteLater)

        self.progress_worker = ProgressWorker(self)
        self.progress_worker.moveToThread(progress_thread)

        progress_thread.started.connect(self.progress_worker.run)
        self.progress_worker.finished.connect(progress_thread.quit)
        self.progress_worker.finished.connect(self.progress_worker.deleteLater)
        progress_thread.finished.connect(progress_thread.deleteLater)
        self.progress_worker.progress.connect(gui_progress_updater)
        self.progress_worker.finished.connect(on_finish)

    def start(self):
        self.bg_task_thread.start()
        self.progress_thread.start()


class ObservableTaskWorker(BackgroundTaskWorker):
    task: ObservableTask

    def __init__(self, task: ObservableTask, progressable: Progressable):
        super().__init__(progressable)
        self.task = task

    @property
    def progress(self):
        return self.task.progress

    def execute(self):
        return self.task.execute()











