from abc import abstractmethod
from typing import Any
from .progress_tracker import ProgressTracker
from .task_result import ObservableTaskResult


class ObservableTask:
    """
    Base class for all long-lasting tasks. Such tasks are meant to be executed via INTERNAL SERVER.
    Using a PROGRESS TRACKER in class implementations is strictly advised. Otherwise, your task probably
    should not be an OBSERVABLE TASK.
    """

    _progress_tracker: ProgressTracker

    @property
    def progress(self) -> float:
        return self._progress_tracker.percentage

    @abstractmethod
    def execute(self) -> ObservableTaskResult:
        """
        This method must be an entry point for performing the required task and must return the result of it.
        """
        raise NotImplementedError()

    @abstractmethod
    def _initialize_progress_units(self):
        """
        Everything connected with setting up a PROGRESS TRACKER must be stored here.
        """
        raise NotImplementedError()
