from typing import Any, Optional
from .model import Model
from ..utils import Parser
from ..api.workspace import Workspace

WORKSPACE = "workspace"


class Manager(Model):
    """
    Manager top class that manages basically
    """

    _lock = 0
    _force_refresh = 0
    fields = []
    nomenclature: str = "Workspace"

    def lock(self) -> None:
        self._lock += 1

    def unlock(self) -> None:
        self._lock -= 1

    def enable_force_refresh(self):
        self._force_refresh += 1

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
        return {getattr(child, "desc"): child.commit() for child in self.workspaces}

    def commit(self) -> None:
        if self.is_locked():
            return

        self.lock()
        Parser.save(self._get_commit_data())
        self.unlock()

    def setup(self) -> None:
        if self.is_locked():
            return

        data = Parser.load()
        self.from_data(data)

    def from_data(self, data: Any) -> None:
        for i, j in data.items():
            child = self.add_child(WORKSPACE, len(self.workspaces))
            child.edit("desc", i)
            child.from_data(j)

    def refresh_data(self) -> bool:
        data_new = Parser.load()
        data_cache = self._get_commit_data()

        if data_new == data_cache:
            if self._force_refresh:
                self._force_refresh -= 1
            else:
                return False

        self.workspaces.clear()
        self.todos.clear()
        self.setup()
        return True


manager = Manager()
manager.setup()
