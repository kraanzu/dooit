from typing import Literal, Optional
from rich.text import TextType, Text
from textual.message import Message

from dooit.api.workspace import Workspace

StatusType = Literal["NORMAL", "INSERT", "DATE", "SEARCH", "SORT", "K PENDING"]
SortMethodType = Literal["description", "status", "date", "urgency"]
EmptyWidgetType = Literal["todo", "workspace", "no_search_results"]
PositionType = Literal["workspace", "todo"]


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


class TopicSelect(Message, bubble=True):
    """
    Emitted when the user selects a todo from search list
    """

    def __init__(self, model: Optional[Workspace] = None) -> None:
        super().__init__()
        self.model = model


class CommitData(Message):
    """
    Emitted when the local data needs to be updated
    """
