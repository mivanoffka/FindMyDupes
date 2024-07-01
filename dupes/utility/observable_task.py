from abc import abstractmethod
from typing import Any


class ObservableTask:
    """
    Base class for all long-lasting tasks. Such tasks are meant to be executed via INTERNAL SERVER.
    Using a PROGRESS TRACKER in class implementations is strictly advised. Otherwise, your task probably
    should not be an OBSERVABLE TASK.
    """

    @abstractmethod
    def execute(self) -> Any:
        """
        This method must be an entry point for performing the required task and must return the result of it.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def progress(self) -> float:
        """
        Using a PROGRESS TRACKER in class implementations is strictly advised. In this case, just return
        ProgressTracker's PROGRESS property to implement this property.
        """
        raise NotImplementedError()

    @abstractmethod
    def _initialize_progress_units(self):
        """
        Everything connected with setting up a PROGRESS TRACKER must be stored here.
        """
        raise NotImplementedError()
