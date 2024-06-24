import concurrent.futures
import os
from abc import abstractmethod
from pathlib import Path

from PIL import Image
from imagehash import ImageHash, phash

from dupes.hash_finder import DupeFinderByHash
import concurrent.futures


class DupeFinderByHashParallelable(DupeFinderByHash):
    @property
    @abstractmethod
    def PoolType(self) -> type:
        raise NotImplementedError()

    def _get_hashmap(self, folder) -> dict[Path, ImageHash]:
        hashmap = {}

        file_paths = folder.file_paths
        file_paths_parted = self._split_list(file_paths, os.cpu_count())

        with self.PoolType() as executor:
            results = list(executor.map(self._thread, file_paths_parted))

        for result in results:
            hashmap.update(result)

        return hashmap

    def _split_list(self, lst, n):
        k, m = divmod(len(lst), n)
        return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]

    def _thread(self, file_paths):
        hmp = {}

        for path in file_paths:
            try:
                hmp[path] = phash(Image.open(path))
            except Exception as error:
                self._log_to_report(f"Could not open or process '{path}'")

            self._progress_tracker.current_value += self._hashing_progress_delta

        return hmp


class DupeFinderByHashMultiThread(DupeFinderByHashParallelable):
    @property
    def PoolType(self) -> type:
        return concurrent.futures.ThreadPoolExecutor


class DupeFinderByHashMultiCore(DupeFinderByHashParallelable):
    @property
    def PoolType(self) -> type:
        return concurrent.futures.ThreadPoolExecutor

