import copy
import os
from datetime import timedelta
from pathlib import Path

from PIL import Image
from imagehash import ImageHash, phash

from dupes.dupefinder import DupeFinder
from dupes.progress_tracker import ProgressTracker
from .exceptions import *

import concurrent.futures
import numpy


# This should have been a DupeFinderByHash derivative class,
# but for an unknown reason using an inherited class from DupeFinderByHash
# that has any override method crashes PyQt threading system

class DupeFinderByHashMultithread(DupeFinder):
    __progress_tracker: ProgressTracker

    __hashing_progress_delta: float
    __grouping_progress_delta: float
    __sorting_progress_delta: float

    def _get_hashmap(self, folder) -> dict[Path, ImageHash]:
        def split_list(lst, n):
            k, m = divmod(len(lst), n)
            return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]

        hashmap = {}

        file_paths = folder.file_paths
        file_paths_parted = split_list(file_paths, os.cpu_count())

        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = list(executor.map(self._hashmapping_thread, file_paths_parted))

        for result in results:
            hashmap.update(result)

        return hashmap

    def _hashmapping_thread(self, file_paths):
        hashmap = {}

        for path in file_paths:
            try:
                hashmap[path] = phash(Image.open(path))
            except Exception as error:
                self._log_to_report(f"Could not open or process '{path}'")

            self.__progress_tracker.current_value += self.__hashing_progress_delta

        return hashmap

    def _sort_hashmap(self, hashmap: dict[Path, ImageHash]) -> dict[Path, ImageHash]:
        if len(hashmap) <= 1:
            return hashmap

        delta_to_finish = self.sorting_component

        hashmap_list = list(hashmap.items())
        stack = [(0, len(hashmap_list) - 1)]

        while stack:
            low, high = stack.pop()

            if low < high:
                pivot_index = (low + high) // 2
                pivot = hashmap_list[pivot_index][1]

                hashmap_list[pivot_index], hashmap_list[high] = hashmap_list[high], hashmap_list[pivot_index]

                store_index = low

                for i in range(low, high):
                    self.__progress_tracker.current_value += self.__sorting_progress_delta
                    delta_to_finish -= self.__sorting_progress_delta

                    if hashmap_list[i][1] - pivot <= 0:
                        hashmap_list[store_index], hashmap_list[i] = hashmap_list[i], hashmap_list[store_index]
                        store_index += 1

                hashmap_list[store_index], hashmap_list[high] = hashmap_list[high], hashmap_list[store_index]

                stack.append((low, store_index - 1))
                stack.append((store_index + 1, high))

        self.__progress_tracker.current_value += delta_to_finish
        return dict(hashmap_list)

    def _group_paths_by_hashes(self, hashmap) -> list:
        groups = []
        current_group = []
        paths = tuple(hashmap.keys())

        for i in range(0, len(paths)):
            current_path = paths[i]
            previous_path = paths[i - 1] if i != 0 else paths[len(paths) - 1]

            previous_hash = hashmap[previous_path]
            current_hash = hashmap[current_path]

            if current_hash - previous_hash <= self.threshold:
                current_group.append(previous_path)
            else:
                if len(current_group) > 0:
                    current_group.append(previous_path)
                    groups.append(copy.copy(current_group))
                    current_group = []

            self.__progress_tracker.current_value += self.__grouping_progress_delta

        if len(current_group) > 0:
            groups.append(copy.copy(current_group))

        return groups

    def execute(self):
        self.__progress_tracker.start()
        hashmaps = (self._get_hashmap(folder) for folder in self._image_folders)

        hashmap_unsorted = {}
        for hashmap in hashmaps:
            for key in hashmap.keys():
                hashmap_unsorted[key] = hashmap[key]

        if len(hashmap_unsorted) == 0:
            raise NoValidImagesError("No images were opened or processed correctly.")

        hashmap_sorted = self._sort_hashmap(hashmap_unsorted)
        groups = self._group_paths_by_hashes(hashmap_sorted)

        self.__progress_tracker.finish()

        return groups

    def _initialize_progress_units(self):
        self.hashing_component = sum(folder.files_count for folder in self._image_folders)
        if self.hashing_component < 2:
            raise EmptyFoldersError("Nothing to compare. Provide at least 2 files in at least 1 folder")

        self.__hashing_progress_delta = 1

        self.sorting_component = self.hashing_component / 2
        self.__sorting_progress_delta = 1 / self.hashing_component / 2

        self.grouping_component = self.hashing_component / 16
        self.__grouping_progress_delta = self.__hashing_progress_delta / 16

        aim_value = self.hashing_component + self.grouping_component + self.sorting_component

        self.__progress_tracker = ProgressTracker(aim_value)

    @property
    def progress(self) -> float:
        return self.__progress_tracker.percentage

    @property
    def threshold(self) -> int:
        return 64 - int(self._precision * 64)

    @property
    def duration(self) -> timedelta:
        return self.__progress_tracker.duration