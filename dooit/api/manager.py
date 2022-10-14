from .model import Model
from typing import Any, Dict, Optional
from ..utils import Parser

WORKSPACE = "workspace"


class Manager(Model):
    """
    Manager top class that manages basically
    """

    fields = []
    nomenclature: str = "Workspace"

    def __init__(self, parent: Optional["Model"] = None) -> None:
        super().__init__(parent)

    def add_child_workspace(self):
        return super().add_child(WORKSPACE)

    def add_sibling_workspace(self):
        return super().add_sibling(WORKSPACE)

    def shift_workspace(self):
        return super().shift_down(WORKSPACE)

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
        Save obj data generated
        """

        data = {getattr(child, "about"): child.commit() for child in self.workspaces}
        Parser.save(data)

    def setup(self):
        """
        Load the storage file and re-create the tree
        """

        data = Parser.load()
        self.from_data(data)

    def from_data(self, data: Any):
        """
        Fill in the attrs from data provided
        """

        for i, j in data.items():
            child = self.add_child(WORKSPACE)
            child.edit("about", i)
            child.from_data(j)


manager = Manager()
manager.setup()
