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
        value = self.model_value

        if value is None:
            return ""

        if value.hour or value.minute:
            return self.model_value.strftime("%Y-%m-%d %H:%M")

        return value.strftime("%Y-%m-%d")

    def _typecast_value(self, value: str) -> Any:
        if not value:
            return None

        due, ok = parse(value)
        if not ok:
            return self.model_value

        return due


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
    def _get_default_value(self) -> str:
        val = self.model_value

        if val == "completed":
            return "x"

        if val == "overdue":
            return "!"

        return "o"

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
