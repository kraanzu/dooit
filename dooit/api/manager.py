from typing import Any, Dict, Optional
from .model import Model
from ..utils import Parser
from ..api.workspace import Workspace

WORKSPACE = "workspace"


class Manager(Model):
    """
    Manager top class that manages basically
    """

    _lock = 0
    fields = []
    nomenclature: str = "Workspace"
    parser_cache = None

    def lock(self) -> None:
        self._lock += 1

    def unlock(self) -> None:
        self._lock -= 1

    def is_locked(self) -> bool:
        return self._lock != 0

    def __init__(self, parent: Optional["Model"] = None) -> None:
        super().__init__(parent)

    def add_child_workspace(self) -> Workspace:
        return super().add_child(WORKSPACE)

    def remove_child_workspace(self, name: str) -> Workspace:
        return super().remove_child(WORKSPACE, name)

    def sort_workspace(self, attr: str) -> None:
        return super().sort(WORKSPACE, attr)

    def _get_commit_data(self):
        return {
            getattr(child, "description"): child.commit() for child in self.workspaces
        }

    def commit(self) -> None:
        if self.is_locked():
            return

        self.lock()
        Parser.save(self._get_commit_data())
        self.unlock()

    def setup(self, data: Optional[Dict] = None) -> None:
        if self.is_locked():
            return

        data = data or Parser.load()
        if data:
            self.from_data(data)

    def from_data(self, data: Any) -> None:
        for i, j in data.items():
            child = self.add_child(WORKSPACE, len(self.workspaces))
            child.edit("description", i)
            child.from_data(j)

    def refresh_data(self) -> bool:
        data_new = Parser.load()

        if not data_new or data_new == self.parser_cache:
            return False

        self.parser_cache = data_new
        current_data = self._get_commit_data()
        if data_new == current_data:
            return False

        self.workspaces.clear()
        self.todos.clear()
        self.setup(data_new)
        return True


manager = Manager()
manager.setup()
