from .progressable import Progressable


class ProgressUnit(Progressable):
    __aim_value: float
    __current_value: float = 0
    __multiplier: float

    @property
    def aim_value(self):
        return self.__aim_value

    @property
    def current_value(self):
        return self.__current_value

    def __set_aim_value(self, aim_value: float):
        if aim_value < 0:
            raise ValueError("Aim value must be greater than or equal to zero")

        self.__aim_value = aim_value

    def increment(self):
        if self.__current_value - 1 <= self.__aim_value:
            self.__current_value += 1

    def decrement(self):
        if self.__current_value - 1 >= 0:
            self.__current_value -= 1

    def reset(self):
        self.__current_value = 0

    def finish(self):
        self.__current_value = self.__aim_value

    def __init__(self, aim_value: float, multiplier: float = 1):
        Progressable.__init__(self, multiplier)
        self.__set_aim_value(aim_value)
