import unittest
from pathlib import Path

from dupes.utility import ObservableTaskResultStatus
from .utilities import create_or_clear_folder, copy_files
from dupes import DupeFinderByHashMultiThread, ImageFolder


class DupeFinderByHashTest(unittest.TestCase):
    parent_folder = Path(__file__).parent
    folder_path = parent_folder / "dynamic_storage"

    def test_one_group(self):
        create_or_clear_folder(self.folder_path)
        copy_files(self.parent_folder / "one_group", self.folder_path)
        finder = DupeFinderByHashMultiThread(ImageFolder(str(self.folder_path)), precision=1)
        groups = finder.execute().value

        result = 0
        if isinstance(groups, list):
            result = len(groups)

        self.assertEqual(result, 1)

    def test_two_groups(self):
        create_or_clear_folder(self.folder_path)
        copy_files(self.parent_folder / "two_groups", self.folder_path)
        finder = DupeFinderByHashMultiThread(ImageFolder(str(self.folder_path)), precision=1)
        groups = finder.execute().value

        result = 0
        if isinstance(groups, list):
            result = len(groups)

        self.assertEqual(result, 2)

    def test_no_duplicates(self):
        create_or_clear_folder(self.folder_path)
        copy_files(self.parent_folder / "no_duplicates", self.folder_path)
        finder = DupeFinderByHashMultiThread(ImageFolder(str(self.folder_path)), precision=1)
        groups = finder.execute().value

        result = 0
        if isinstance(groups, list):
            result = len(groups)

        self.assertEqual(result, 0)

    def test_three_duplicates(self):
        create_or_clear_folder(self.folder_path)
        copy_files(self.parent_folder / "one_group", self.folder_path)
        finder = DupeFinderByHashMultiThread(ImageFolder(str(self.folder_path)), precision=1)
        groups = finder.execute().value

        result = 0
        if isinstance(groups, list):
            for group in groups:
                result += len(group)

        self.assertEqual(result, 3)

    def test_four_duplicates(self):
        create_or_clear_folder(self.folder_path)
        copy_files(self.parent_folder / "two_groups", self.folder_path)
        finder = DupeFinderByHashMultiThread(ImageFolder(str(self.folder_path)), precision=1)
        groups = finder.execute().value

        result = 0
        if isinstance(groups, list):
            for group in groups:
                result += len(group)

        self.assertEqual(result, 4)

    def test_partial_status(self):
        create_or_clear_folder(self.folder_path)
        copy_files(self.parent_folder / "corrupted", self.folder_path)
        finder = DupeFinderByHashMultiThread(ImageFolder(str(self.folder_path)), precision=1)
        status = finder.execute().status

        self.assertEqual(status, ObservableTaskResultStatus.PARTIAL)

    def test_corrupted_folder(self):
        create_or_clear_folder(self.folder_path)
        copy_files(self.parent_folder / "corrupted", self.folder_path)
        finder = DupeFinderByHashMultiThread(ImageFolder(str(self.folder_path)), precision=1)
        warnings = len(finder.execute().logs)

        self.assertEqual(warnings, 2)


if __name__ == "__main__":
    unittest.main()
