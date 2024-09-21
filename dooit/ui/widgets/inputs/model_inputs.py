from typing import Any

from .simple_input import SimpleInput
from dooit.api import Todo, Workspace
from dooit.utils import parse


class TodoDescription(SimpleInput[Todo]):
    @property
    def _property(self) -> str:
        return "description"


class WorkspaceDescription(SimpleInput[Workspace]):
    @property
    def _property(self) -> str:
        return "description"


class Due(SimpleInput[Todo]):
    def start_edit(self) -> None:
        self._value = None
        return super().start_edit()

    def _typecast_value(self, value: str) -> Any:
        if not value:
            return None

        return parse(value)


class Urgency(SimpleInput[Todo]):
    @property
    def value(self) -> str:
        res = self.model.urgency

        if res == 0:
            return ""

        return str(self.model.urgency)

    def _typecast_value(self, value: str) -> Any:
        if not value or value == "0":
            return None

        return int(value)


class Effort(SimpleInput[Todo]):
    def _typecast_value(self, value: str) -> Any:
        if not value or value == "0":
            return None

        return int(value)


class Status(SimpleInput[Todo]):
    def _typecast_value(self, value: str) -> Any:
        if value == "COMPLETED":
            return False

        return True


class Recurrence(SimpleInput[Todo]):
    @property
    def value(self) -> str:
        res = self.model.recurrence

        if res is None:
            return ""

        return str(res)
