from typing import Literal
from rich.text import TextType, Text
from textual.message import Message, MessageTarget

StatusType = Literal["NORMAL", "INSERT", "DATE", "SEARCH", "SORT", "K PENDING"]
SortMethodType = Literal["description", "status", "date", "urgency"]


class ExitApp(Message, bubble=True):
    """
    Emitted when user presses the exit app keybind
    """


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

    def __init__(self, status: StatusType) -> None:
        super().__init__()
        self.status: StatusType = status


class Notify(Message, bubble=True):
    """
    Emitted when A notification message on status bar is to be shown
    """

    def __init__(self, message: TextType) -> None:
        super().__init__()
        if isinstance(message, Text):
            message = message.markup
        self.message = message


class ApplySortMethod(Message, bubble=True):
    """
    Emitted when the user selects a sort method from sort-menu
    """

    def __init__(self, widget_obj: str, method: str) -> None:
        super().__init__()
        self.method = method
        self.widget_obj = widget_obj


class TopicSelect(Message, bubble=True):
    """
    Emitted when the user selects a todo from search list
    """

    def __init__(self, item) -> None:
        super().__init__()
        self.item = item
