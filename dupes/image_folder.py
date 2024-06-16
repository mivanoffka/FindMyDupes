from pathlib import Path
from typing import Optional, Iterable


class ImageFolder:
    _folder_path: str
    _allowed_file_formats: tuple[str] = ["*.jpg", "*.jpeg"]
    _file_formats_filter = Optional[list[str]]

    @property
    def folder_path(self):
        return self._folder_path

    @property
    def selected_file_formats(self) -> tuple[str]:
        selected_file_formats = []
        if self._file_formats_filter is None:
            selected_file_formats = self._allowed_file_formats
        else:
            for file_format in self._file_formats_filter:
                if file_format in self._allowed_file_formats:
                    selected_file_formats.append(file_format)

                else:
                    raise AttributeError(f"Invalid file format '{file_format}'."
                                         f" Valid formats are: {self._allowed_file_formats}")

        return tuple(selected_file_formats)

    @property
    def file_paths(self) -> tuple[Path, ...]:
        file_paths = []

        for file_format in self.selected_file_formats:
            file_paths.extend(list(Path(self._folder_path).glob(file_format)))

        return tuple(file_paths)

    def __init__(self, folder_path: str, file_formats_filter: Optional[Iterable[str]] = None):
        self._folder_path = folder_path
        self._file_formats_filter = file_formats_filter


if __name__ == "__main__":
    img_folder = ImageFolder("/Users/mivanoffka/Pictures/df_test/1")
    print(img_folder.selected_file_formats)
    print(img_folder.folder_path)
    print(img_folder.file_paths)

