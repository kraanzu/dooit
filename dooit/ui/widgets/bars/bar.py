from collections.abc import Callable
from typing import List, Optional
from rich.console import RenderableType
from rich.text import TextType
from rich.table import Table
from dooit.ui.events.events import DooitEvent
from ._base import BarBase


class BarWidget:
    def __init__(
        self, func: Callable[..., TextType], width: Optional[int] = None
    ) -> None:
        self.func = func
        self.width = width
        self.value = self.calculate()

    def calculate(self) -> TextType:
        self.value = self.func()
        return self.value

    def get_value(self):
        return self.value


class Bar(BarBase):
    bar_widgets = []

    def set_widgets(self, widgets: List[BarWidget]) -> None:
        self.bar_widgets = widgets
        self.refresh()

    def trigger_event(self, event: DooitEvent):
        pass

    def render(self) -> RenderableType:
        expand = any(widget.width == 0 for widget in self.bar_widgets)
        table = Table.grid(expand=expand, padding=0)

        for widget in self.bar_widgets:
            value = widget.get_value()
            if widget.width is None:
                table.add_column(width=len(value))
            elif width := widget.width:
                table.add_column(width=width)
            else:
                table.add_column(ratio=1)

        values = [widget.get_value() for widget in self.bar_widgets]
        table.add_row(*values)

        return table
