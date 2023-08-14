from typing import Any, Dict, Optional
from ..api.todo import Todo
from .model import Model

WORKSPACE = "workspace"
TODO = "todo"


class Workspace(Model):
    fields = ["description"]
    sortable_fields = ["description"]

    def __init__(self, parent: Optional["Model"] = None) -> None:
        from .model_items import Description

        super().__init__(parent)
        self._description = Description(self)

    @property
    def description(self):
        return self._description.value

    def add_workspace(self, index: int = 0) -> "Workspace":
        return super().add_child(WORKSPACE, index)

    def add_todo(self, index: int = 0) -> Todo:
        return super().add_child(TODO, index)

    def commit(self) -> Dict[str, Any]:
        child_workspaces = [
            workspace.commit() for workspace in self.workspaces if workspace.description
        ]

        todos = [todo.commit() for todo in self.todos if todo.description]

        return {
            "uuid": self.uuid,
            "description": self.description,
            "todos": todos,
            "workspaces": child_workspaces,
        }

    # WARNING: This will be deprecated in future versions
    def extract_data_old(self, data: Dict):
        for i, j in data.items():
            if i == "common":
                for k in j:
                    todo = self.add_todo(index=len(self.todos))
                    todo.from_data(k)
                continue

            workspace = self.add_child("workspace", index=len(self.workspaces))
            workspace.edit("description", i)
            workspace.from_data(j)

    def extract_data_new(self, data: Dict, overwrite_uuid: bool):
        if overwrite_uuid:
            self._uuid = data["uuid"]

        self._description.set(data["description"])

        for todo in data["todos"]:
            child_todo = self.add_todo(index=len(self.todos))
            child_todo.from_data(todo, overwrite_uuid)

        for workspace in data["workspaces"]:
            child_workspace = self.add_workspace(len(self.workspaces))
            child_workspace.from_data(workspace, overwrite_uuid)

    def from_data(self, data: Any, overwrite_uuid: bool = True) -> None:
        if isinstance(data, dict):
            if "uuid" not in data:
                self.extract_data_old(data)
            else:
                self.extract_data_new(data, overwrite_uuid)

        elif isinstance(data, list):
            todo = self.add_todo(index=len(self.todos))
            todo.from_data(data, overwrite_uuid)
