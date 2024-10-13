from typing import List
from rich.console import RenderableType
from rich.table import Table

from .._base import BarBase
from .bar_widget import StatusBarWidget


class StatusBar(BarBase):
    bar_widgets = []

    def set_widgets(self, widgets: List[StatusBarWidget]) -> None:
        self.bar_widgets = widgets
        self.refresh()

    def render(self) -> RenderableType:
        expand = any(widget.width == 0 for widget in self.bar_widgets)
        table = Table.grid(expand=expand, padding=0)

        for widget in self.bar_widgets:
            value = widget.render()
            if widget.width is None:
                table.add_column(width=len(value))
            elif width := widget.width:
                table.add_column(width=width)
            else:
                table.add_column(ratio=1)

        values = [widget.render() for widget in self.bar_widgets]
        table.add_row(*values)

        return table
