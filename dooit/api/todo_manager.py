from typing import Literal, Optional, List

from dooit.utils import Urgency
from dooit.utils.workspace import WorkSpace

SortMethodType = Literal["name", "status", "date", "urgency"]
FilterMethod = Literal["about", "date", "urgency"]


class Manager:
    """
    A Manager backend for dooit
    """

    def __init__(self) -> None:
        self.workspaces: List[WorkSpace] = []

    def add_workspace(self, workspace: str):
        new_workspace = WorkSpace(workspace)
        self.workspaces.append(new_workspace)

    def _get_workspace_index(self, workspace: str) -> int:
        return [i for i, j in enumerate(self.workspaces) if j.name == workspace][0]

    def get_workspace(self, workspace: str) -> WorkSpace:
        idx = self._get_workspace_index(workspace)
        return self.workspaces[idx]

    def rename_workspace(self, workspace: str, name: str) -> None:
        self.get_workspace(workspace).name = name

    def remove_workspace(self, workspace: str):
        idx = self._get_workspace_index(workspace)
        self.workspaces.pop(idx)

    def add_topic(self, workspace: str, topic: str):
        self.get_workspace(workspace).add_topic(topic)

    def rename_topic(self, workspace: str, topic: str, name: str):
        self.get_workspace(workspace).rename_topic(topic, name)

    def remove_topic(self, workspace: str, topic):
        self.get_workspace(workspace).remove_topic(topic)

    def add_todo(
        self,
        workspace: str,
        topic: str = "common",
        about: Optional[str] = None,
        due: Optional[str] = None,
        urgency: Optional[Urgency] = None,
    ):
        self.get_workspace(workspace).add_todo(topic, about, due, urgency)

    def remove_todo(
        self,
        id_: str,
        workspace: str,
        topic: str = "common",
    ):
        ...

    def edit_todo(
        self,
        id_: str,
        workspace: str,
        topic: str = "common",
        about: Optional[str] = None,
        due: Optional[str] = None,
        urgency: Optional[Urgency] = None,
    ):
        self.get_workspace(workspace).edit_todo(id_, topic, about, due, urgency)

    def sort_todos(self):
        ...

    def filter_todos(self):
        ...


MANAGER = Manager()
