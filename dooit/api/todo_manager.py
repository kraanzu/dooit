from datetime import datetime
from typing import Literal, Optional, Union

from dooit.utils import Urgency, WorkSpace

DateType = Union[str, datetime]
SortMethodType = Literal["name", "status", "date", "urgency"]
FilterMethod = Literal["about", "date", "urgency"]


class Manager:
    """
    A Manager backend for dooit
    """

    def __init__(self) -> None:
        self.workspaces: dict[str, WorkSpace] = dict()

    def add_workspace(self, workspace: str):
        self.workspaces[workspace] = WorkSpace(workspace)

    def rename_workspace(self, workspace: str, name: str):
        self.workspaces[name] = self.workspaces[workspace]
        del self.workspaces[workspace]

    def remove_workspace(self, workspace: str):
        del self.workspaces[workspace]

    def add_topic(self, workspace: str, topic: str):
        self.workspaces[workspace].add_topic(topic)

    def rename_topic(self, workspace: str, topic: str, name: str):
        self.workspaces[workspace].rename_topic(topic, name)

    def remove_topic(self, workspace: str, topic):
        self.workspaces[workspace].remove_topic(topic)

    def add_todo(
        self,
        workspace: str,
        topic: str = "common",
        about: Optional[str] = None,
        due: Optional[DateType] = None,
        urgency: Optional[Urgency] = None,
    ):
        self.workspaces[workspace].add_todo(topic, about, due, urgency)

    def edit_todo(
        self,
        id_: str,
        workspace: str,
        topic: str = "common",
        about: Optional[str] = None,
        due: Optional[DateType] = None,
        urgency: Optional[Urgency] = None,
    ):
        self.workspaces[workspace].edit_todo(id_, topic, about, due, urgency)

    def sort_todos(
        self,
        workspace: str,
        *,
        topic: str = "common",
        method: SortMethodType,
    ):
        ...

    def filter_todos(
        self, workspace: str, *, topic: str = "common", method: FilterMethod
    ):
        ...


MANAGER = Manager()
