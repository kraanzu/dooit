from rich.align import Align
from rich.console import RenderableType
from rich.panel import Panel
from rich.style import StyleType
from textual.widget import Widget


class Box(Widget):
    def __init__(
        self,
        name: str | None = None,
        color: StyleType = "blue",
    ) -> None:
        super().__init__(name)
        self.color = color
        self.highlighted = False

    def render(self) -> RenderableType:
        return Panel(
            Align.center(self.name, vertical="middle"),
            border_style=("bold " if self.highlighted else "dim ") + str(self.color),
            height=3,
        )

    def highlight(self):
        self.highlighted = True
        self.refresh()

    def lowlight(self):
        self.highlighted = False
        self.refresh()
