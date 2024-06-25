from abc import abstractmethod
from datetime import timedelta
from typing import Any


class ObservableTask:
    __report: list[str]

    def _log_to_report(self, message: str):
        self.__report.append(message)

    @property
    def report(self) -> tuple:
        return tuple(self.__report)

    @abstractmethod
    def execute(self) -> Any:
        raise NotImplementedError()

    @property
    @abstractmethod
    def progress(self) -> float:
        raise NotImplementedError()

    @property
    @abstractmethod
    def duration(self) -> timedelta:
        raise NotImplementedError()

    @abstractmethod
    def _initialize_progress_units(self):
        raise NotImplementedError()
