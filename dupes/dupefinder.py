from abc import ABCMeta, abstractmethod
from pathlib import Path

from dupes.image_folder import ImageFolder


class DupeFinder(metaclass=ABCMeta):
    _image_folders: tuple[ImageFolder]
    _precision: float

    @property
    @abstractmethod
    def progress(self) -> float:
        raise NotImplementedError

    @property
    def image_folders(self) -> tuple[ImageFolder]:
        return self._image_folders

    @property
    def precision(self) -> float:
        return self._precision

    @abstractmethod
    def search(self):
        raise NotImplementedError

    @abstractmethod
    def _initialize_progress_units(self):
        raise NotImplementedError

    def __init__(self, *image_folders: ImageFolder, precision: float):
        if not (0 <= precision <= 1):
            raise ValueError("Precision must be in range [0, 1]")
        self._precision = precision
        self._image_folders = (*image_folders, )
        self._initialize_progress_units()


