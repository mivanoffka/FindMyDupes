from typing import Any, Optional
from .statuses import Status


class Result:
    _value: Any
    _status: Status
    _logs: Optional[tuple]
    _message: str

    @property
    def value(self) -> Any:
        return self._value

    @property
    def status(self) -> Status:
        return self._status

    @property
    def logs(self) -> Optional[tuple]:
        return self._logs

    @property
    def message(self) -> str:
        return self._message

    def __init__(self, value, status, logs, message):
        self._value = value
        self._status = status
        self._logs = logs
        self._message = message

