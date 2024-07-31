from time import time
from typing import Any, Dict, List, Optional
from .model import Model
from ..utils import Parser
from ..api.workspace import Workspace

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

    def add_workspace(self) -> Workspace:
        return self.add_child("workspace")

    def _get_commit_data(self) -> Any:
        return [child._get_commit_data() for child in self.workspaces]

    def commit(self) -> bool:

        if self.is_locked():
            return False

        self.lock()
        self.last_modified = time()
        parser.save(self._get_commit_data())
        self.unlock()
        return True

    def setup(self, data: Optional[Dict] = None) -> None:
        if self.is_locked():
            return

        data = data or parser.load()
        if not data:
            return

        self.workspaces.clear()
        self.todos.clear()
        self.last_modified = parser.last_modified
        self.from_data(data)

    def __extract_data(self, data: List):
        for i in data:
            child = self.add_child(WORKSPACE, len(self.workspaces))
            child.from_data(i)

    def from_data(self, data: Any) -> None:
        self.__extract_data(data)

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
