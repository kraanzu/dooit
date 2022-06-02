from typing import Literal
from textual.widgets import NodeID
from textual.message import Message, MessageTarget

StatusType = Literal["NORMAL", "INSERT", "DATE", "SEARCH"]
DueType = Literal["COMPLETED", "PENDING", "OVERDUE"]


class MenuOptionChange(Message, bubble=True):
    def __init__(self, sender: MessageTarget, option: str) -> None:
        super().__init__(sender)
        self.option = option


class ChangeStatus(Message, bubble=True):
    def __init__(self, sender: MessageTarget, status: StatusType) -> None:
        super().__init__(sender)
        self.status = status


class Notify(Message, bubble=True):
    def __init__(self, sender: MessageTarget, message: str) -> None:
        super().__init__(sender)
        self.message = message


class ModifyTopic(Message, bubble=True):
    def __init__(self, sender: MessageTarget, old: str, new: str) -> None:
        super().__init__(sender)
        self.old = old
        self.new = new


class ApplySortMethod(Message, bubble=True):
    def __init__(self, sender: MessageTarget, method: str) -> None:
        super().__init__(sender)
        self.method = method


class HighlightNode(Message, bubble=True):
    def __init__(self, sender: MessageTarget, id: NodeID) -> None:
        super().__init__(sender)
        self.id = id
