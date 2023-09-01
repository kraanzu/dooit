from typing import Literal
from rich.align import Align
from rich.console import Group, RenderableType
from textual.widget import Widget
from dooit.utils.conf_reader import config_man
from .aligner import align_texts

EmptyWidgetType = Literal["todo", "workspace", "no_search_results", "dashboard"]


DASHBOARD, EMPTY_TODO, EMPTY_WORKSPACE, NO_SEARCH_RESULTS = [
    align_texts(
        config_man.get(i),
    )
    for i in ["DASHBOARD", "EMPTY_TODO", "EMPTY_WORKSPACE", "no_search_results"]
]


class EmptyWidget(Widget):
    item = DASHBOARD

    def __init__(self, item: EmptyWidgetType = "dashboard"):
        classes = "no-border" if item != "dashboard" else ""
        super().__init__(classes=classes)
        self.set_screen(item)

    def set_screen(self, screen: EmptyWidgetType) -> None:
        if screen == "todo":
            self.item = EMPTY_TODO
        elif screen == "workspace":
            self.item = EMPTY_WORKSPACE
        elif screen == "no_search_results":
            self.item = NO_SEARCH_RESULTS
        elif screen == "dashboard":
            self.item = DASHBOARD
        else:
            self.item = []

        self.refresh()

    def render(self) -> RenderableType:
        return Align.center(
            Group(*[Align.center(i) for i in self.item]),
            vertical="middle",
        )
