from pathlib import Path
from typing import Optional, Iterable


ALLOWED_FILE_FORMATS: tuple = ("*.jpg", "*.png", "*.bmp", "*.tiff", "*.gif", "*.ico")


class ImageFolder:
    """
    A class to contain information about the folder to observe and which files to select using FILE FORMATS FILTER.
    If you want to extract all possible file formats (specified in ALLOWED_FILE_FORMATS), set the filter to NONE
    """

    _folder_path: str
    _file_formats_filter = Optional[list[str]]


    @property
    def folder_path(self):
        return self._folder_path

    @property
    def file_formats_filter(self) -> Optional[list[str]]:
        return self._file_formats_filter

    @file_formats_filter.setter
    def file_formats_filter(self, value):
        self._file_formats_filter = value

    @property
    def _selected_file_formats(self) -> tuple[str]:
        """
        Only returns formats that match both FILE_FORMATS_FILTER and ALLOWED_FILE_FORMAT
        """
        selected_file_formats = []
        if self._file_formats_filter is None:
            selected_file_formats = ALLOWED_FILE_FORMATS
        else:
            for file_format in self._file_formats_filter:
                if file_format in ALLOWED_FILE_FORMATS:
                    selected_file_formats.append(file_format)

                else:
                    raise AttributeError(f"Invalid file format '{file_format}'."
                                         f" Valid formats are: {ALLOWED_FILE_FORMATS}")

        return tuple(selected_file_formats)

    @property
    def file_paths(self) -> tuple[Path, ...]:
        """
        Returns paths to all the files that match FILE FORMAT FILTER
        """
        file_paths = []

        for file_format in self._selected_file_formats:
            file_paths.extend(list(Path(self._folder_path).glob(file_format)))

        return tuple(file_paths)

    @property
    def files_count(self) -> int:
        return len(self.file_paths)

    def __init__(self, folder_path: str, file_formats_filter: Optional[Iterable[str]] = None):
        self._folder_path = folder_path
        self._file_formats_filter = file_formats_filter

