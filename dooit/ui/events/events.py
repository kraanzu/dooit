from typing import Callable, Literal, Optional
from textual.message import Message

from dooit.api.model import DooitModel, SortMethodType
from dooit.api import Workspace

ModeType = Literal["NORMAL", "INSERT", "DATE", "SEARCH", "SORT", "K PENDING", "CONFIRM"]
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


class StartSearch(DooitEvent):
    """
    Emitted when user wants to search
    """

    def __init__(self, callback: Callable) -> None:
        super().__init__()
        self.callback = callback


class StartSort(DooitEvent):
    """
    Emitted when user wants to sort
    """

    def __init__(self, model: DooitModel) -> None:
        super().__init__()
        self.model = model


class ShowConfirm(DooitEvent):
    """
    Emitted when confirmation from user is required
    """

    def __init__(self, callback: Callable) -> None:
        super().__init__()
        self.callback = callback
