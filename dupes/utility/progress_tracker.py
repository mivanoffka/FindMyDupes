import logging


class ProgressTracker:
    __aim_value: float
    __current_value: float = 0

    __report: list[str] = []

    def log_to_report(self, message: str):
        logging.warning(message)
        self.__report.append(message)

    @property
    def report(self) -> tuple:
        return tuple(self.__report)

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
        if 0 <= value <= self.__aim_value:
            self.__current_value = value
        elif value < 0:
            self.__current_value = 0
        else:
            self.__current_value = self.__aim_value

    def __set_aim_value(self, aim_value: float):
        if aim_value <= 0:
            raise ValueError("Aim value must be greater than zero")

        self.__aim_value = aim_value

    def reset(self):
        self.__current_value = 0

    def finish(self):
        self.__current_value = self.__aim_value

    def __init__(self, aim_value: float):
        self.__set_aim_value(aim_value)
