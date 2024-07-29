from collections.abc import Callable
from typing import List, Optional
from rich.console import RenderableType
from rich.text import TextType
from rich.table import Table
from textual.widget import Widget


class BarWidget:
    def __init__(self, func: Callable[..., TextType], width: Optional[int]) -> None:
        self.func = func
        self.width = width
        self.value = self.calculate()

    def calculate(self) -> TextType:
        self.value = self.func()
        return self.value

    def get_value(self):
        return self.value


class Bar(Widget):
    DEFAULT_CSS = """
    Bar {
        height: 1;
    }
    """
    bar_widgets = []

    def set_widgets(self, widgets: List[BarWidget]) -> None:
        self.bar_widgets = widgets

    def render(self) -> RenderableType:
        table = Table.grid(expand=True)

        for widget in self.bar_widgets:
            if widget.width is None:
                table.add_column("", ratio=1)
            elif width := widget.width:
                table.add_column("", width=width)
            else:
                table.add_column("")

        return table
