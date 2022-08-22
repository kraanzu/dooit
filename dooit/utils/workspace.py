from typing import Optional, Literal

from dooit.api.todo_manager import DateType
from dooit.utils import Topic
from dooit.utils.urgency import Urgency


ResponseType = Literal["OK", "ERROR", "WARNING"]


class Response:
    def __init__(self, code: ResponseType, msg: str) -> None:
        self.code = code
        self.msg = msg


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

    def add_topic(self, topic: str) -> Response:

        if topic in self.topics:
            return Response("ERROR", "Already present")

        self.topics[topic] = Topic(topic)
        return Response("ERROR", "Already present")

    def rename_topic(self, topic: str, name) -> Response:

        if topic in self.topics:
            return Response("ERROR", "Already present")

        self.topics[name] = self.topics[topic]
        self.topics[name].rename(name)
        self.remove_topic(topic)

        return Response("OK", "Topic removed")

    def add_todo(
        self,
        topic: str = "common",
        about: Optional[str] = None,
        due: Optional[str] = None,
        urgency: Optional[Urgency] = None,
    ):
        self.topics[topic].add_todo(about, due, urgency)

    def edit_todo(
        self,
        id_: str,
        topic: str = "common",
        about: Optional[str] = None,
        due: Optional[str] = None,
        urgency: Optional[Urgency] = None,
    ):
        self.topics[topic].edit_todo(id_, about, due, urgency)
