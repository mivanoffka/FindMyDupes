import socket
import time
from abc import abstractmethod
from datetime import timedelta, datetime

from PySide6.QtCore import Signal, QObject

from server import InternalServerManager
from dupes import ObservableTask
from . import IWidgetForShowingProgress
from .message_window import MessageWindow


class _BackgroundTaskWorker(QObject):

    """
    Objects of this class are only meant to be inherited by
    InternalServerBackgroundTask so that _ProgressWorker could be included and
    defined before InternalServerBackgroundTask.

    Do not create instances of this class manually!
    """

    finished: Signal = Signal()
    result = None

    @abstractmethod
    def execute(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def duration(self) -> timedelta:
        raise NotImplementedError()

    def run(self):
        try:
            self.result = self.execute()

        except Exception as error:
            MessageWindow.show_error(str(error))

        self.finished.emit()


class _ProgressWorker(QObject):

    """
    Objects of this class are only meant to be included and define
    a loop that will track and update progress indicators in a WidgetForShowingProgress

    Do not create instances of this class manually!
    """

    bg_worker: _BackgroundTaskWorker
    progress = Signal(float)
    finished = Signal(object)

    client: socket.socket

    def __init__(self, bg_worker: _BackgroundTaskWorker):
        super().__init__()
        self.bg_worker = bg_worker

    def run(self):
        while self.bg_worker.result is None:
            percentage = round(InternalServerManager().get_current_task_progress() * 100, 1)
            if percentage >= 0:
                self.progress.emit(percentage)
            time.sleep(0.1)

        self.progress.emit(100)
        time.sleep(0.1)
        self.finished.emit((self.bg_worker.result, self.bg_worker.duration))


class InternalServerBackgroundTask(_BackgroundTaskWorker):

    """
    This class can be used to execute an ObservableTask and track its progress
    without interrupting the GUI mainloop, yet the way of parallel execution is not implemented.

    If you want to execute your ObservableTask via InternalServer, use the InternalServerBackgroundTask

    You need a widget or window that follows IWidgetForShowingProgress
    to display progress tracking properly.
    """

    _progress_worker: _ProgressWorker
    _task: ObservableTask

    _start_time: datetime
    _finish_time: datetime

    @property
    def duration(self) -> timedelta:
        return self._finish_time - self._start_time

    def __init__(self, task: ObservableTask, window: IWidgetForShowingProgress):
        super().__init__()
        self._task = task
        self._connect_to_widget(window)

    def _connect_to_widget(self, widget: IWidgetForShowingProgress):
        bg_task_thread = widget.task_thread
        progress_thread = widget.progress_thread
        gui_progress_updater = widget.update_progress
        on_finish = widget.on_task_finish

        self.bg_task_thread = bg_task_thread
        self.progress_thread = progress_thread

        self.moveToThread(bg_task_thread)

        self.finished.connect(bg_task_thread.quit)
        self.finished.connect(self.deleteLater)

        bg_task_thread.started.connect(self.run)
        bg_task_thread.finished.connect(bg_task_thread.deleteLater)

        self._progress_worker = _ProgressWorker(self)
        self._progress_worker.moveToThread(progress_thread)

        progress_thread.started.connect(self._progress_worker.run)
        self._progress_worker.finished.connect(progress_thread.quit)
        self._progress_worker.finished.connect(self._progress_worker.deleteLater)
        progress_thread.finished.connect(progress_thread.deleteLater)
        self._progress_worker.progress.connect(gui_progress_updater)
        self._progress_worker.finished.connect(on_finish)

    def start(self):
        self.bg_task_thread.start()
        self.progress_thread.start()

    def execute(self):
        self._start_time = datetime.now()
        result = InternalServerManager().execute_task(self._task)
        self._finish_time = datetime.now()

        return result















