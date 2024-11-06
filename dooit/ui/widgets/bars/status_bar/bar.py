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
        row = []

        for widget in self.bar_widgets:
            value = widget.render()
            row.append(value)

            if widget.width is None:
                if len(value):
                    table.add_column(width=len(value))
                else:
                    row.pop()  # pragma: no cover

            elif width := widget.width:
                table.add_column(width=width)
            else:
                table.add_column(ratio=1)

        table.add_row(*row)
        return table
