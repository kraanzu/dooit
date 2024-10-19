from datetime import timedelta, datetime
from typing import Callable, Literal, Optional
from textual.message import Message

from dooit.api.model import DooitModel
from dooit.api import Workspace, Todo

ModeType = Literal["NORMAL", "INSERT", "DATE", "SEARCH", "SORT", "K PENDING", "CONFIRM"]
EmptyWidgetType = Literal["todo", "workspace", "no_search_results"]
PositionType = Literal["workspace", "todo"]


# Super event


class DooitEvent(Message, bubble=True):
    """
    Base class for all events
    """


# Base events


class WorkspaceEvent(DooitEvent):
    """
    Base class for all workspace events
    """


class TodoEvent(DooitEvent):
    """
    Base class for all todo events
    """


# Events


class Startup(DooitEvent):
    """
    Emitted when the app starts
    """


class ShutDown(DooitEvent):
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

    def __init__(self, mode: ModeType) -> None:
        super().__init__()
        self.mode: ModeType = mode


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


# Workspace events


class WorkspaceSelected(WorkspaceEvent):
    """
    Emitted when user selects a workspace
    """

    def __init__(self, workspace: Workspace) -> None:
        super().__init__()
        self.workspace = workspace


class WorkspaceRemoved(WorkspaceEvent):
    """
    Emitted when user removes a workspace
    """

    def __init__(self, workspace: Workspace) -> None:
        super().__init__()
        self.workspace = workspace


class WorkspaceDescriptionChanged(WorkspaceEvent):
    """
    Emitted when user changes the description of a workspace
    """

    def __init__(self, old: str, new: str, workspace: Workspace) -> None:
        super().__init__()
        self.old = old
        self.new = new
        self.workspace = workspace


# Todo events


class TodoSelected(TodoEvent):
    """
    Emitted when user selects a todo
    """

    def __init__(self, todo: Todo) -> None:
        super().__init__()
        self.todo = todo


class TodoRemoved(TodoEvent):
    """
    Emitted when user removes a todo
    """

    def __init__(self, todo: Todo) -> None:
        super().__init__()
        self.todo = todo


class TodoDescriptionChanged(TodoEvent):
    """
    Emitted when user changes the description of a todo
    """

    def __init__(self, old: str, new: str, todo: Todo) -> None:
        super().__init__()
        self.old = old
        self.new = new
        self.todo = todo


class TodoDueChanged(TodoEvent):
    """
    Emitted when user changes the due of a todo
    """

    def __init__(
        self, old: Optional[datetime], new: Optional[datetime], todo: Todo
    ) -> None:
        super().__init__()
        self.old = old
        self.new = new
        self.todo = todo


class TodoStatusChanged(TodoEvent):
    """
    Emitted when user changes the status of a todo
    """

    def __init__(self, old: str, new: str, todo: Todo) -> None:
        super().__init__()
        self.old = old
        self.new = new
        self.todo = todo


class TodoEffortChanged(TodoEvent):
    """
    Emitted when user changes the effort of a todo
    """

    def __init__(self, old: Optional[int], new: Optional[int], todo: Todo) -> None:
        super().__init__()
        self.old = old
        self.new = new
        self.todo = todo


class TodoRecurrenceChanged(TodoEvent):
    """
    Emitted when user changes the recurrence of a todo
    """

    def __init__(
        self, old: Optional[timedelta], new: Optional[timedelta], todo: Todo
    ) -> None:
        super().__init__()
        self.old = old
        self.new = new
        self.todo = todo


class TodoUrgencyChanged(TodoEvent):
    """
    Emitted when user changes the urget of a todo
    """

    def __init__(self, old: int, new: int, todo: Todo) -> None:
        super().__init__()
        self.old = old
        self.new = new
        self.todo = todo
