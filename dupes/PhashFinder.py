from pathlib import Path
from random import random

from PIL import Image
import imagehash
from imagehash import ImageHash, phash

from dupes.image_folder import ImageFolder
from findable import Findable

import numpy


class PhashFinder(Findable):
    def _get_hashmap_single_thread(self, image_folder) -> dict[Path, ImageHash]:
        hashmap = {}
        paths = image_folder.file_paths
        percent = 100 / len(paths)
        percentage = 0
        aim = 0

        for path in image_folder.file_paths:
            if percentage >= aim:
                print(f"{int(percentage)}%")
                aim += 1

            image: Image = Image.open(path)
            hash_value = phash(image)

            hashmap[path] = hash_value
            percentage += percent

        return self._sort_hashmap(hashmap)

    def _sort_hashmap(self, hashmap) -> dict:
        only_hashes = [hashmap[path] for path in hashmap.keys()]
        only_hashes_sorted = self.hash_quick_sort(only_hashes)

        hashmap_sorted = {}
        for hash in only_hashes_sorted:
            path = next(key for key, value in hashmap.items() if value == hash)
            hashmap.pop(path)
            hashmap_sorted[path] = hash

        return hashmap_sorted

    def _group_paths_by_hashes(self, hashmap) -> list:
        # for s in [f"{str(hashmap[key])} : {key}" for key in hashmap.keys()]:
        #     print(s)
        groups = []
        current_group = []
        paths = tuple(hashmap.keys())
        for i in range(0, len(paths)):
            current_path = paths[i]
            previous_path = paths[i-1] if i != 0 else paths[len(paths)-1]

            previous_hash = hashmap[previous_path]
            current_hash = hashmap[current_path]

            if abs(current_hash - previous_hash) < 1:
                current_group.append(previous_path)
            else:
                if len(current_group) > 0:
                    current_group.append(previous_path)
                    groups.append(current_group)
                    current_group = []

        for group in groups:
             print(group)
        return groups

    def hash_quick_sort(self, hashes: list[ImageHash]) -> list[ImageHash]:
        if len(hashes) <= 1:
            return hashes

        pivot = hashes[len(hashes) // 2]
        left = [x for x in hashes if x - pivot < 0]
        middle = [x for x in hashes if x == pivot]
        right = [x for x in hashes if x - pivot > 0]

        return self.hash_quick_sort(left) + middle + self.hash_quick_sort(right)

    def _find_duplicates_for_two_folders(self, first_image_folder: ImageFolder, second_image_folder: ImageFolder):
        pass

    def _find_duplicates_for_single_folder(self, image_folder: ImageFolder):
        hashmap = self._get_hashmap_single_thread(image_folder)
        groups = self._group_paths_by_hashes(hashmap)
        print(f"{len(groups)} groups of duplicates found")


if __name__ == "__main__":
    phash_finder = PhashFinder()
    image_folder = ImageFolder("/Users/mivanoffka/Pictures/Datasets/flower_images/LillyS")
    phash_finder.find_duplicates(image_folder)

