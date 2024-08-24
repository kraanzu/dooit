from dooit.api.todo import Todo
from dooit.api.workspace import Workspace
from .simple_input import SimpleInput


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
        self.value = ""
        return super().start_edit()


class Urgency(SimpleInput): ...


class Effort(SimpleInput): ...


class Status(SimpleInput): ...


class Recurrence(SimpleInput): ...
