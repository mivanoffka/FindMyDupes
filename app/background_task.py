import struct
from abc import abstractmethod
import time
from datetime import timedelta, datetime
from typing import Any

from dupes import DupeFinder, ObservableTask
from .utilities import display_message

from PySide6.QtCore import Signal, QObject, QThread
from .progressdisplay import ProgressDisplay

import socket
import threading
import json
import pickle


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

    @property
    @abstractmethod
    def duration(self) -> timedelta:
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

    def _get_progress(self) -> float:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('127.0.0.1', 9999))

            data = pickle.dumps("GET_PROGRESS")
            len_data = struct.pack('>I', len(data))

            client.send(len_data)
            client.send(data)

            msglen = struct.unpack('>I', client.recv(4))[0]
            response = client.recv(msglen)
            result = pickle.loads(response)
            client.close()
            return result
        except Exception as e:
            print(e)

        return 0

    def run(self):
        while self.bg_worker.result is None:
            percentage = round(self._get_progress() * 100, 1)
            self.progress.emit(percentage)
            time.sleep(0.1)

        print('finished!!!')
        self.progress.emit(100)
        time.sleep(0.1)
        self.finished.emit((self.bg_worker.result, self.bg_worker.duration))


class BackgroundTaskWorker(BackgroundTaskWorkerDefinition):
    progress_worker: ProgressWorker

    @abstractmethod
    def execute(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def progress(self) -> float:
        raise NotImplementedError()

    def __init__(self, progressable: ProgressDisplay):
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
        self.progress_thread.start()
        self.bg_task_thread.start()



class ObservableTaskWorker(BackgroundTaskWorker):
    task: ObservableTask

    def __init__(self, task: ObservableTask, progressable: ProgressDisplay):
        super().__init__(progressable)
        self.task = task

    @property
    def progress(self):
        return self.task.progress

    @property
    def duration(self) -> timedelta:
        return self.finish_time - self.start_time

    def execute(self):
        try:
            self.start_time = datetime.now()
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('127.0.0.1', 9999))
            client.settimeout(10000)

            data = pickle.dumps(self.task)
            len_data = struct.pack('>I', len(data))

            client.send(len_data)
            client.send(data)

            msglen = struct.unpack('>I', client.recv(4))[0]
            response = client.recv(msglen)
            result = pickle.loads(response)

            client.close()
            self.finish_time = datetime.now()
            return result
        except Exception as e:
            print(e)











