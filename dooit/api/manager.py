from time import time
from typing import Any, List, Dict, Optional
from .model import Model
from ..utils import Parser
from ..api.workspace import Workspace
from ..api.todo import Todo

WORKSPACE = "workspace"
parser = Parser()

class Manager(Model):
    """
    Manager top class that manages basically
    """

    _lock = 0
    fields = []
    nomenclature: str = "Workspace"
    last_modified = 0

    def lock(self) -> None:
        self._lock += 1

    def unlock(self) -> None:
        self._lock -= 1

    def is_locked(self) -> bool:
        return self._lock != 0

    def __init__(self, parent: Optional["Model"] = None) -> None:
        super().__init__(parent)
        self.workspaces: List[Workspace] = []

    def add_child(self, kind: str, index: int = 0, inherit: bool = False) -> Any:
      child = Workspace(parent=self)
      self.workspaces.append(child)
      return child

    def _get_children(self, kind: str) -> List:
        return self.workspaces

    def _get_commit_data(self):
        return {
            getattr(child, "description"): child.commit() for child in self.workspaces
        }

    def commit(self) -> None:
        if self.is_locked():
            return

        self.lock()
        self.last_modified = time()
        parser.save(self._get_commit_data())
        self.unlock()

    def setup(self, data: Optional[Dict] = None) -> None:
        if self.is_locked():
            return

        data = data or parser.load()
        if not data:
            return

        self.workspaces.clear()
        self.last_modified = parser.last_modified
        self.from_data(data)

    def from_data(self, data: Any) -> None:
        for i, j in data.items():
            child = self.add_child(WORKSPACE)
            child.edit("description", i)
            child.from_data(j)

    def refresh_data(self) -> bool:

        if abs(self.last_modified - parser.last_modified) <= 2:
            return False

        if self.last_modified > parser.last_modified:
            self.commit()
            return False

        self.setup()
        return True


manager = Manager()
manager.setup()
