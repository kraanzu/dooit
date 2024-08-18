from typing import Literal, Optional
from textual.message import Message
from dooit.api.model import SortMethodType
from dooit.api.workspace import Workspace

ModeType = Literal["NORMAL", "INSERT", "DATE", "SEARCH", "SORT", "K PENDING"]
EmptyWidgetType = Literal["todo", "workspace", "no_search_results"]
PositionType = Literal["workspace", "todo"]


class DooitEvent(Message, bubble=True):
    """
    Base class for all events
    """

    kwargs = {}

    @property
    def snake_case(self):
        name = self.__class__.__name__
        joined = "".join(["_" + i.lower() if i.isupper() else i for i in name])
        return joined.lstrip("_")


class Startup(DooitEvent):
    """
    Emitted when the app starts
    """


class ExitApp(DooitEvent):
    """
    Emitted when user presses the exit app keybind
    """


class SwitchTab(DooitEvent):
    """
    Emitted when user needs to focus other pane
    """


class SpawnHelp(DooitEvent):
    """
    Emitted when user presses `?` in NORMAL mode
    """


class ModeChanged(DooitEvent):
    """
    Emitted when there is a change in the `status`
    """

    def __init__(self, status: ModeType) -> None:
        super().__init__()
        self.status: ModeType = status


class TopicSelect(DooitEvent):
    """
    Emitted when the user selects a todo from search list
    """

    def __init__(self, model: Optional[Workspace] = None) -> None:
        super().__init__()
        self.model = model


class ApplySort(DooitEvent):
    """
    Emitted when the user wants to sort a tree
    """

    def __init__(self, query: str, widget_id: str, method: SortMethodType) -> None:
        super().__init__()
        self.query = query
        self.widget_id = widget_id
        self.method = method
