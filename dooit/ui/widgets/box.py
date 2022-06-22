from rich.box import SQUARE_DOUBLE_HEAD
from rich.console import RenderableType
from rich.panel import Panel
from rich.style import StyleType
from rich.table import Table
from rich.text import Text
from textual.widget import Widget

from ...utils.config import conf


class Box(Widget):
    """
    A simple widget to render text with a panel
    """

    def __init__(
        self,
        name: str | None = None,
        options: list[str] = [],
        color: StyleType = "blue",
    ) -> None:
        super().__init__(name=name)
        self.options = options
        self.color = color
        self.highlighted = False
        config = conf.load_config()
        self.style_highlighted = config["header_highlight"]
        self.style_dim = config["header_dim"]

    def render(self) -> RenderableType:
        table = Table.grid(padding=(0, 1), expand=True)
        style = self.style_highlighted if self.highlighted else self.style_dim

        for i in self.options:
            table.add_column(i, justify="center", ratio=1)

        table.add_row(*[Text(name, style=style) for name in self.options])

        return Panel(table, border_style=style, height=3, box=SQUARE_DOUBLE_HEAD)

    def highlight(self) -> None:
        self.highlighted = True
        self.refresh()

    def lowlight(self) -> None:
        self.highlighted = False
        self.refresh()
