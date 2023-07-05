from typing import Any, Dict, Optional
from ..api.todo import Todo
from .model import Model
from .item_concrete_creator import ItemConcreteCreator

WORKSPACE = "workspace"
TODO = "todo"


class Workspace(Model):
    fields = ["description"]
    sortable_fields = ["description"]

    def __init__(self, parent: Optional["Model"] = None) -> None:

        super().__init__(parent)
        itemCreator = ItemConcreteCreator()
        self._description = itemCreator.create_description(self)

    @property
    def path(self):
        parent_path = self.parent.path if self.parent else ""
        return self.description + "#" + parent_path

    @property
    def description(self):
        return self._description.value

    def add_workspace(self, index: int = 0):
        return super().add_child(WORKSPACE, index)

    def add_todo(self, index: int = 0) -> Todo:
        return super().add_child(TODO, index)

    def commit(self) -> Dict[str, Any]:
        child_workspaces = {
            workspace.description: workspace.commit()
            for workspace in self.workspaces
            if workspace.description
        }

        todos = {"common": [todo.commit() for todo in self.todos if todo.description]}

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
                workspace.edit("description", i)
                workspace.from_data(j)

        elif isinstance(data, list):
            todo = self.add_todo(index=len(self.todos))
            todo.from_data(data)
