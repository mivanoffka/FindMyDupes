from abc import abstractmethod, ABCMeta


class Progressable(metaclass=ABCMeta):
    # I have no idea how do you implement public getter but private setter otherwise :(
    __mp: float = 1.0

    @property
    def multiplier(self) -> float:
        return self._multiplier

    @property
    def _multiplier(self) -> float:
        return self.__mp

    @_multiplier.setter
    def _multiplier(self, value: float):
        if value < 0:
            raise ValueError("Multiplier must be greater than or equal to zero")

        self.__mp = value

    @property
    @abstractmethod
    def current_value(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def aim_value(self) -> float:
        raise NotImplementedError

    @property
    def percentage(self) -> float:
        return self.current_value / self.aim_value

    def __init__(self, multiplier: float = 1):
        self._multiplier = multiplier

