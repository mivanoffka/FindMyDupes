from pathlib import Path

from PIL import Image
from imagehash import ImageHash, phash

from dupes.image_folder import ImageFolder
from dupes.dupefinder import DupeFinder

from abc import ABCMeta, abstractmethod

from dupes.progress_tracker import ProgressTracker


class DupeFinderByHash(DupeFinder):
    __progress_tracker: ProgressTracker

    __hashing_progress_delta: float
    __grouping_progress_delta: float
    __sorting_progress_delta: float

    @abstractmethod
    def _hash(self, image: Image):
        raise NotImplementedError

    def _get_hashmap(self, folder) -> dict[Path, ImageHash]:
        hashmap = {}

        for path in folder.file_paths:
            hashmap[path] = self._hash(Image.open(path))
            self.__progress_tracker.current_value += self.__hashing_progress_delta

        return hashmap

    def _sort_hashmap(self, hashmap: dict[Path, ImageHash]):
        if len(hashmap) <= 1:
            return hashmap

        pivot = list(hashmap.values())[len(hashmap) // 2]

        left = {path: hashmap[path] for path in hashmap.keys()
                if hashmap[path] - pivot == 0}
        right = {path: hashmap[path] for path in hashmap.keys()
                 if hashmap[path] - pivot > 0}

        return left | self._sort_hashmap(right)

    def _group_paths_by_hashes(self, hashmap) -> list:
        groups = []
        current_group = []
        paths = tuple(hashmap.keys())

        for i in range(0, len(paths)):
            current_path = paths[i]
            previous_path = paths[i-1] if i != 0 else paths[len(paths)-1]

            previous_hash = hashmap[previous_path]
            current_hash = hashmap[current_path]

            if current_hash - previous_hash < 1:
                current_group.append(previous_path)
            else:
                if len(current_group) > 0:
                    current_group.append(previous_path)
                    groups.append(current_group)
                    current_group = []

            self.__progress_tracker.current_value += self.__grouping_progress_delta

        return groups

    def start_searching(self):
        hashmap_unsorted = self._get_hashmap(self._image_folders[0])

        hashmap_sorted = self._sort_hashmap(hashmap_unsorted)
        self.__progress_tracker.current_value += self.__sorting_progress_delta

        groups = self._group_paths_by_hashes(hashmap_sorted)

        return groups

    def _initialize_progress_units(self):
        hashing_component = sum(folder.files_count for folder in self._image_folders)
        self.__hashing_progress_delta = 1

        grouping_component = hashing_component / 25
        self.__grouping_progress_delta = 1 / 25

        sorting_component = hashing_component / 8
        self.__sorting_progress_delta = sorting_component

        aim_value = hashing_component + grouping_component + sorting_component

        self.__progress_tracker = ProgressTracker(aim_value)

    @property
    def progress(self) -> float:
        return self.__progress_tracker.percentage


if __name__ == "__main__":
    image_folder = ImageFolder("/Users/mivanoffka/Pictures/Datasets/flower_images/LillyS")
    phash_finder = DupeFinderByHash(image_folder)
    phash_finder.start_searching()
