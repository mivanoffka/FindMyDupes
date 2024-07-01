from abc import abstractmethod
from datetime import timedelta
from typing import Any


class ObservableTask:
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
