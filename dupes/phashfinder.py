from PIL.Image import Image

from dupes import DupeFinderByHash
from imagehash import phash


class DupeFinderByPhash(DupeFinderByHash):
    def _hash(self, image: Image):
        return phash(image)
