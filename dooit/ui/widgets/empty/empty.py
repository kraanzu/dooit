from typing import List, Literal, Optional
from rich.align import Align
from rich.console import Group, RenderableType
from textual.widget import Widget

EmptyWidgetType = Literal["todo", "workspace", "no_search_results", "dashboard"]


class EmptyWidget(Widget):
    item: List[RenderableType]

    def __init__(self, id: Optional[str] = None):
        super().__init__(id=id)

    def render(self) -> RenderableType:
        return Align.center(
            Group(*[Align.center(i) for i in self.item]),
            vertical="middle",
        )


class Dashboard(EmptyWidget):
    item = [""]


class EmptyTodoWidget(EmptyWidget):
    item = [""]


class EmptyWorkspaceWidget(EmptyWidget):
    item = [""]


class NoSearchResultsWidget(EmptyWidget):
    item = [""]


# ----------------- #

WORKSPACE_EMPTY_WIDGETS = [
    EmptyWorkspaceWidget(id="empty-workspace"),
    NoSearchResultsWidget(id="no-search-results-workspace"),
]
TODO_EMPTY_WIDGETS = [
    Dashboard(id="dashboard"),
    EmptyTodoWidget(id="empty-todo"),
    NoSearchResultsWidget(id="no-search-results-todo"),
]
