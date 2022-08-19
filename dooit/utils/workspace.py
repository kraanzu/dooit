from typing import Optional

from dooit.api.todo_manager import DateType
from dooit.utils import Topic
from dooit.utils.urgency import Urgency


class WorkSpace:
    """
    WorkSpace Manager
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.topics: dict[str, Topic] = dict()
        self.topics["common"] = Topic("common")

    def remove_topic(self, topic: str) -> None:
        del self.topics[topic]

    def add_topic(self, topic: str) -> None:
        self.topics[topic] = Topic(topic)

    def rename_topic(self, topic: str, name) -> None:
        self.topics[name] = self.topics[topic]
        self.topics[name].rename(name)
        self.remove_topic(topic)

    def add_todo(
        self,
        topic: str = "common",
        about: Optional[str] = None,
        due: Optional[DateType] = None,
        urgency: Optional[Urgency] = None,
    ):
        self.topics[topic].add_todo(about, due, urgency)

    def edit_todo(
        self,
        id_: str,
        topic: str = "common",
        about: Optional[str] = None,
        due: Optional[DateType] = None,
        urgency: Optional[Urgency] = None,
    ):
        self.topics[topic].edit_todo(id_, about, due, urgency)
