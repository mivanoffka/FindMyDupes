from typing import Optional

from dupes.exceptions import TaskNotStartedError
from datetime import datetime, timedelta


class ProgressTracker:
    __aim_value: float
    __current_value: float = -1

    __start_time: Optional[datetime] = None
    __finish_time: Optional[datetime] = None

    @property
    def duration(self) -> timedelta:
        max_time = datetime.now() if self.__finish_time is None else self.__finish_time
        return max_time - self.__start_time

    @property
    def aim_value(self):
        return self.__aim_value

    @property
    def current_value(self):
        return self.__current_value

    @property
    def percentage(self):
        return self.current_value / self.aim_value

    @current_value.setter
    def current_value(self, value: float):
        if self.__current_value < 0:
            raise TaskNotStartedError("The task is not in progress. Use the 'start()' method.")

        if 0 <= value <= self.__aim_value:
            self.__current_value = value
        elif value < 0:
            self.__current_value = 0
        else:
            self.__current_value = self.__aim_value

    def __set_aim_value(self, aim_value: float):
        if aim_value <= 0:
            raise ValueError("Aim value must be greater than zer0")

        self.__aim_value = aim_value

    def start(self):
        self.__current_value = 0
        self.__start_time = datetime.now()

    def reset(self):
        self.__current_value = -1

    def finish(self):
        self.__current_value = self.__aim_value
        self.__finish_time = datetime.now()

    def __init__(self, aim_value: float):
        self.__set_aim_value(aim_value)
