from dupes.progress.progress_unit import ProgressUnit
from .progressable import Progressable


class ProgressTracker(Progressable):
    __progress_units: dict[str, Progressable]

    @property
    def percentage(self) -> float:
        return self.current_value / self.aim_value

    @property
    def current_value(self) -> float:
        return sum(unit.multiplier * unit.percentage for unit in self.__progress_units.values())

    @property
    def aim_value(self) -> float:
        return sum(unit.multiplier for unit in self.__progress_units.values())

    def __getitem__(self, key: str) -> Progressable:
        return self.__progress_units[key]

    def __init__(self, multiplier: float = 1.0, **progress_units: ProgressUnit):
        Progressable.__init__(self, multiplier)
        self.__progress_units = progress_units
