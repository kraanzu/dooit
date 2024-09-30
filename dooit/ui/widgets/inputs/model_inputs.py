from datetime import datetime
from typing import Any

from .simple_input import SimpleInput
from dooit.api import Todo, Workspace
from dooit.utils import parse


class TodoDescription(SimpleInput[Todo, str]):
    @property
    def _property(self) -> str:
        return "description"


class WorkspaceDescription(SimpleInput[Workspace, str]):
    @property
    def _property(self) -> str:
        return "description"


class Due(SimpleInput[Todo, datetime]):
    def _get_default_value(self) -> str:
        if self.model_value is None:
            return ""

        return self.model_value.strftime("%Y-%m-%d %H:%M")

    def start_edit(self) -> None:
        self._value = ""
        return super().start_edit()

    def _typecast_value(self, value: str) -> Any:
        if not value:
            return None

        return parse(value)


class Urgency(SimpleInput[Todo, int]):
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


class Effort(SimpleInput[Todo, int]):
    def _typecast_value(self, value: str) -> Any:
        if not value or value == "0":
            return None

        return int(value)


class Status(SimpleInput[Todo, str]):
    def _typecast_value(self, value: str) -> Any:
        if value == "COMPLETED":
            return False

        return True


class Recurrence(SimpleInput[Todo, datetime]):
    @property
    def value(self) -> str:
        res = self.model.recurrence

        if res is None:
            return ""

        return str(res)
