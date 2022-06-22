from rich.console import RenderableType
from rich.text import Text
from textual.widget import Widget

from ...utils.config import conf


class Border(Widget):
    """
    Widget to serve as borders
    """

    def __init__(
        self, name: str | None = None, color: str = "blue", item="", measure="width"
    ) -> None:
        super().__init__(name)
        self.highlight = False
        self.color = color
        self.item = item
        self.measure = measure
        config = conf.load_config()
        self.style_highlight = config["body_highlight"]
        self.style_dim = config["body_dim"]

    def toggle_highlight(self) -> None:
        self.highlight = not self.highlight
        self.refresh()

    def illuminate(self) -> None:
        self.highlight = True
        self.refresh()

    def dim(self) -> None:
        self.highlight = False
        self.refresh()

    def render(self) -> RenderableType:
        count = self.size.width if self.measure == "width" else self.size.height
        style = self.style_highlight if self.highlight else self.style_dim
        return Text(self.item * count, style=style)


class HorizontalLine(Border):
    """
    Draws a horizontal line w.r.t to its width
    """

    def __init__(self) -> None:
        super().__init__(item="━")


class VerticalLine(Border):
    """
    Draws a vertical line w.r.t to its height
    """

    def __init__(self) -> None:
        super().__init__(item="┃\n", measure="height")


class Connector1(Border):
    """
    Connects left and top border
    """

    def __init__(self) -> None:
        super().__init__(item="┏")

    def render(self) -> RenderableType:
        width = self.size.width - 1
        height = self.size.height - 1
        if width:
            self.item += "━" * width
        if height:
            self.item += "\n┃" * height

        style = "bold blue" if self.highlight else "dim white"
        return Text(self.item, style=style)


class Connector2(Border):
    """
    Connects right and top border
    """

    def __init__(self) -> None:
        super().__init__(item="┓")

    def render(self) -> RenderableType:
        width = self.size.width - 2
        height = self.size.height - 1
        if width:
            self.item = "━" * width + self.item
        if height:
            self.item += "\n┃" * height

        style = "bold blue" if self.highlight else "dim white"
        return Text(self.item, style=style)


class Connector3(Border):
    """
    Connects left and bottom border
    """

    def __init__(self) -> None:
        super().__init__(item="┗")

    def render(self) -> RenderableType:
        width = self.size.width - 1
        height = self.size.height - 1
        if width:
            self.item += "━" * width
        if height:
            self.item += "\n┃" * height

        style = "bold blue" if self.highlight else "dim white"
        return Text(self.item, style=style)


class Connector4(Border):
    """
    Connects right and bottom border
    """

    def __init__(self) -> None:
        super().__init__(item="┛")

    def render(self) -> RenderableType:
        width = self.size.width - 2
        height = self.size.height - 1
        if width:
            self.item = "━" * width + self.item
        if height:
            self.item += "\n┃" * height

        style = "bold blue" if self.highlight else "dim white"
        return Text(self.item, style=style)
