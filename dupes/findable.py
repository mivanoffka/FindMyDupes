from abc import ABCMeta, abstractmethod
from pathlib import Path

from dupes.image_folder import ImageFolder


class Findable(metaclass=ABCMeta):

    @abstractmethod
    def _find_duplicates_for_single_folder(self, image_folder: ImageFolder):
        raise NotImplementedError

    @abstractmethod
    def _find_duplicates_for_two_folders(self, first_image_folder: ImageFolder, second_image_folder: ImageFolder):
        raise NotImplementedError

    def find_duplicates(self, *image_folders: ImageFolder):
        if len(image_folders) == 1:
            return self._find_duplicates_for_single_folder(image_folders[0])
        elif len(image_folders) == 2:
            return self._find_duplicates_for_two_folders(*image_folders)
        elif len(image_folders) == 0:
            raise ValueError("No image folders were given. Please provide one or two folders.")
        else:
            raise ValueError("Too many image folders were given. Please provide one or two folders.")


class FindableImpl(Findable):
    def _find_duplicates_for_single_folder(self, image_folder: ImageFolder):
        pass

    def _find_duplicates_for_two_folders(self, first_image_folder: ImageFolder, second_image_folder: ImageFolder):
        pass


if __name__ == '__main__':
    finder = FindableImpl()
