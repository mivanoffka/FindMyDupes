from abc import ABCMeta, abstractmethod
from pathlib import Path

from dupes.image_folder import ImageFolder


class DupeFinder(metaclass=ABCMeta):
    _image_folders: tuple[ImageFolder]

    @property
    def image_folders(self) -> tuple[ImageFolder]:
        return self._image_folders

    def __init__(self, *image_folders: ImageFolder):
        self._image_folders = (*image_folders, )

    @abstractmethod
    def start_searching(self):
        raise NotImplementedError
