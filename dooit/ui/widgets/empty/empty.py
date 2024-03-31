from typing import List, Literal, Optional
from rich.align import Align
from rich.console import Group, RenderableType
from textual.widget import Widget
from dooit.utils.conf_reader import config_man
from ..aligner import align_texts

EmptyWidgetType = Literal["todo", "workspace", "no_search_results", "dashboard"]


DASHBOARD, EMPTY_TODO, EMPTY_WORKSPACE, NO_SEARCH_RESULTS = [
    align_texts(
        config_man.get(i),
    )
    for i in ["DASHBOARD", "EMPTY_TODO", "EMPTY_WORKSPACE", "no_search_results"]
]


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
    item = DASHBOARD


class EmptyTodoWidget(EmptyWidget):
    item = EMPTY_TODO


class EmptyWorkspaceWidget(EmptyWidget):
    item = EMPTY_WORKSPACE


class NoSearchResultsWidget(EmptyWidget):
    item = NO_SEARCH_RESULTS
