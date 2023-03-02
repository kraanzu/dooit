from typing import Literal
from rich.text import TextType, Text
from textual.message import Message, MessageTarget

StatusType = Literal["NORMAL", "INSERT", "DATE", "SEARCH", "SORT", "K PENDING"]
SortMethodType = Literal["description", "status", "date", "urgency"]


class SwitchTab(Message, bubble=True):
    """
    Emitted when user needs to focus other pane
    """


class SpawnHelp(Message, bubble=True):
    """
    Emitted when user presses `?` in NORMAL mode
    """


class ChangeStatus(Message, bubble=True):
    """
    Emitted when there is a change in the `status`
    """

    def __init__(self, sender: MessageTarget, status: StatusType) -> None:
        super().__init__(sender)
        self.status: StatusType = status


class Notify(Message, bubble=True):
    """
    Emitted when A notification message on status bar is to be shown
    """

    def __init__(self, sender: MessageTarget, message: TextType) -> None:
        super().__init__(sender)
        if isinstance(message, Text):
            message = message.markup
        self.message = message


class ApplySortMethod(Message, bubble=True):
    """
    Emitted when the user selects a sort method from sort-menu
    """

    def __init__(self, sender: MessageTarget, method: str) -> None:
        super().__init__(sender)
        self.method = method


class TopicSelect(Message, bubble=True):
    """
    Emitted when the user selects a todo from search list
    """

    def __init__(self, sender: MessageTarget, item) -> None:
        super().__init__(sender)
        self.item = item
