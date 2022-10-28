from typing import Any, Optional
from .model import Model
from ..utils import Parser
from dooit.api.workspace import Workspace

WORKSPACE = "workspace"


class Manager(Model):
    """
    Manager top class that manages basically
    """

    fields = []
    nomenclature: str = "Workspace"

    def __init__(self, parent: Optional["Model"] = None) -> None:
        super().__init__(parent)

    def add_child_workspace(self) -> Workspace:
        return super().add_child(WORKSPACE)

    def add_sibling_workspace(self) -> Workspace:
        return super().add_sibling(WORKSPACE)

    def shift_workspace(self) -> None:
        return super().shift_down(WORKSPACE)

    def next_workspace(self) -> Optional[Workspace]:
        return super().next_sibling(WORKSPACE)

    def prev_workspace(self) -> Optional[Workspace]:
        return super().prev_sibling(WORKSPACE)

    def remove_child_workspace(self, name: str) -> Workspace:
        return super().remove_child(WORKSPACE, name)

    def drop_workspace(self) -> None:
        return super().drop(WORKSPACE)

    def sort_workspace(self, attr: str) -> None:
        return super().sort(WORKSPACE, attr)

    def commit(self) -> None:
        """
        Save obj data generated
        """

        data = {getattr(child, "about"): child.commit() for child in self.workspaces}
        Parser.save(data)

    def setup(self) -> None:
        """
        Load the storage file and re-create the tree
        """

        data = Parser.load()
        self.from_data(data)

    def from_data(self, data: Any) -> None:
        """
        Fill in the attrs from data provided
        """

        for i, j in data.items():
            child = self.add_child(WORKSPACE)
            child.edit("about", i)
            child.from_data(j)


manager = Manager()
manager.setup()
