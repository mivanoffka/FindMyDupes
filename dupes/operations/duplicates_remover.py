import os
from pathlib import Path
from typing import Any

from ..utility import ObservableTask, ProgressTracker
from ..utility.task_result import ObservableTaskResult
from ..utility.statuses import ObservableTaskResultStatus


class DuplicatesRemover(ObservableTask):
    _files_path: list
    _duplicate_groups: list

    def __init__(self, duplicate_groups: list):
        self._duplicate_groups = duplicate_groups
        self._files_path = self._select_files()
        self._initialize_progress_units()

    def _remove_path_from_groups(self, path):
        for group in self._duplicate_groups:
            group: list = group
            if path in group:
                group.remove(path)

    def _select_files(self) -> list:
        files_path = []
        for group in self._duplicate_groups:
            for path in group[1:]:
                files_path.append(path)

        return files_path

    def _initialize_progress_units(self):
        self._progress_tracker = ProgressTracker(len(self._files_path))

    def _remove_files(self):
        deleted_files = 0
        for file_path in self._files_path:
            try:
                os.remove(file_path)
                deleted_files += 1
                self._remove_path_from_groups(file_path)
            except Exception as error:
                self._progress_tracker.log_to_report(f"Unable to delete {file_path}:\r\n{error}")
            self._progress_tracker.current_value += 1

        if deleted_files == 0:
            return ObservableTaskResult(self._duplicate_groups, ObservableTaskResultStatus.FAILED, self._progress_tracker.report, "Не удалось выполнить операцию.")
        elif deleted_files == len(self._files_path):
            return ObservableTaskResult(self._duplicate_groups, ObservableTaskResultStatus.SUCCESS, None, "Операция выполнена успешно.")
        else:
            return ObservableTaskResult(self._duplicate_groups, ObservableTaskResultStatus.PARTIAL, self._progress_tracker, "Операция выполнена лишь частично.")


    def execute(self):
        return self._remove_files()











