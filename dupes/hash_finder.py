from pathlib import Path

from PIL import Image
from imagehash import ImageHash, phash

from dupes.image_folder import ImageFolder
from dupes.dupefinder import DupeFinder


class HashDupeFinder(DupeFinder):

    def _get_hashmap(self, folder) -> dict[Path, ImageHash]:
        hashmap = {}
        for path in folder.file_paths:
            hashmap[path] = phash(Image.open(path))

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

        return groups

    def start_searching(self):
        hashmap_unsorted = self._get_hashmap(self._image_folders[0])
        hashmap_sorted = self._sort_hashmap(hashmap_unsorted)
        groups = self._group_paths_by_hashes(hashmap_sorted)

        return groups

    def _initialize_progress_units(self):
        ...

    @property
    def progress(self) -> float:
        return 0


if __name__ == "__main__":
    image_folder = ImageFolder("/Users/mivanoffka/Pictures/Datasets/flower_images/LillyS")
    phash_finder = HashDupeFinder(image_folder)
    phash_finder.start_searching()
