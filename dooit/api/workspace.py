from typing import Optional
from .model import Model

WORKSPACE = "workspace"
TODO = "todo"


class Workspace(Model):
    fields = ["about"]

    def __init__(self, parent: Optional["Model"] = None) -> None:
        super().__init__(parent)
        self.about = ""

    def add_child_todo(self):
        return super().add_child(TODO)

    def add_sibling_todo(self):
        return super().add_sibling(TODO)

    def shift_todo_up(self):
        return super().shift_up(TODO)

    def shift_todo_down(self):
        return super().shift_down(TODO)

    def next_todo(self):
        return super().next_sibling(TODO)

    def prev_todo(self):
        return super().prev_sibling(TODO)

    def remove_child_todo(self, name: str):
        return super().remove_child(TODO, name)

    def drop_todo(self):
        return super().drop(TODO)

    def sort_todo(self, attr: str):
        return super().sort_children(TODO, attr)

    def add_child_workspace(self):
        return super().add_child(WORKSPACE)

    def add_sibling_workspace(self):
        return super().add_sibling(WORKSPACE)

    def shift_workspace_down(self):
        return super().shift_down(WORKSPACE)

    def shift_workspace_up(self):
        return super().shift_up(WORKSPACE)

    def next_workspace(self):
        return super().next_sibling(WORKSPACE)

    def prev_workspace(self):
        return super().prev_sibling(WORKSPACE)

    def remove_child_workspace(self, name: str):
        return super().remove_child(WORKSPACE, name)

    def drop_workspace(self):
        return super().drop(WORKSPACE)

    def sort_workspace(self, attr: str):
        return super().sort_children(WORKSPACE, attr)

    def commit(self):
        """
        Create obj data to be saved
        """

        child_workspaces = {
            getattr(child, "about"): child.commit() for child in self.workspaces
        }
        todos = {
            "common": [todo.commit() for todo in self.todos],
        }

        return {
            **child_workspaces,
            **todos,
        }

    def from_data(self, data):
        """
        Setup object from stored data
        """

        for i, j in data.items():
            if i == "common":
                for data in j:
                    self.add_child_todo()
                    self.todos[-1].from_data(data)
            else:
                self.add_child_workspace()
                self.workspaces[-1].edit("about", i)
                self.workspaces[-1].from_data(j)
