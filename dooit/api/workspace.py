from typing import Any, Dict, Optional
from ..api.todo import Todo
from .model import Model, Ok, Err, Result

WORKSPACE = "workspace"
TODO = "todo"


class Workspace(Model):
    fields = ["desc"]

    @property
    def path(self):
        parent_path = self.parent.path if self.parent else ""
        return self.desc + "#" + parent_path

    @property
    def desc(self):
        return self._desc

    def set_desc(self, value: str) -> Result:
        if value:
            new_index = -1
            if self.parent:
                new_index = self.parent._get_child_index("workspace", desc=value)

            old_index = self._get_index("workspace")

            if new_index != -1 and new_index != old_index:
                return Err(
                    "A workspace with same description is already present",
                )
            else:
                self._desc = value
                return Ok()

        return Err(
            "Can't leave description empty!",
        )

    def __init__(self, parent: Optional["Model"] = None) -> None:
        super().__init__(parent)
        self._desc = ""

    def add_todo(self, index: int = 0) -> Todo:
        return super().add_child(TODO, index)

    def commit(self) -> Dict[str, Any]:
        child_workspaces = {
            getattr(
                workspace,
                "desc",
            ): workspace.commit()
            for workspace in self.workspaces
        }

        todos = {
            "common": [todo.commit() for todo in self.todos],
        }

        return {
            **todos,
            **child_workspaces,
        }

    def from_data(self, data: Any) -> None:
        if isinstance(data, dict):
            for i, j in data.items():
                if i == "common":
                    for data in j:
                        todo = self.add_todo(index=len(self.todos))
                        todo.from_data(data)
                    continue

                workspace = self.add_child("workspace", index=len(self.workspaces))
                workspace.edit("desc", i)
                workspace.from_data(j)

        elif isinstance(data, list):
            todo = self.add_todo(index=len(self.todos))
            todo.from_data(data)
