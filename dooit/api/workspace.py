from typing import Any, Dict, Optional
from ..api.todo import Todo
from .model import Model

WORKSPACE = "workspace"
TODO = "todo"


class Workspace(Model):
    fields = ["about"]

    def __init__(self, parent: Optional["Model"] = None) -> None:
        super().__init__(parent)
        self.about = ""

    def add_todo(self) -> Todo:
        return super().add_child(TODO)

    def add_workspace(self) -> "Workspace":
        return super().add_child(WORKSPACE)

    def add_sibling(self) -> "Workspace":
        return super().add_sibling(WORKSPACE)

    def shift_down(self) -> None:
        return super().shift_down(WORKSPACE)

    def shift_up(self) -> None:
        return super().shift_up(WORKSPACE)

    def next_sibling(self) -> Optional["Workspace"]:
        return super().next_sibling(WORKSPACE)

    def prev_sibling(self) -> Optional["Workspace"]:
        return super().prev_sibling(WORKSPACE)

    def drop(self) -> None:
        return super().drop(WORKSPACE)

    def sort(self, attr: str) -> None:
        return super().sort(WORKSPACE, attr)

    def commit(self) -> Dict[str, Any]:
        child_workspaces = {
            getattr(
                workspace,
                "about",
            ): workspace.commit()
            for workspace in self.workspaces
        }

        todos = {
            "common": [todo.commit() for todo in self.todos],
        }

        return {
            **child_workspaces,
            **todos,
        }

    def from_data(self, data: Any) -> None:
        if isinstance(data, dict):
            for i, j in data.items():
                if i == "common":
                    for data in j:
                        todo = self.add_todo()
                        todo.from_data(data)
                    continue

                workspace = self.add_workspace()
                workspace.edit("about", i)
                workspace.from_data(j)

        elif isinstance(data, list):
            todo = self.add_todo()
            todo.from_data(data)
