from rich.console import RenderableType
from rich.text import Text
from textual.widget import Widget


class Border(Widget):
    def __init__(
        self, name: str | None = None, color: str = "blue", item="", measure="width"
    ) -> None:
        super().__init__(name)
        self.highlight = False
        self.color = color
        self.item = item
        self.measure = measure

    def toggle_highlight(self):
        self.highlight = not self.highlight
        self.refresh()

    def render(self) -> RenderableType:

        count = self.size.width if self.measure == "width" else self.size.height
        style = "bold " if self.highlight else "dim "
        return Text(self.item * count, style=style + self.color)


class Empty(Border):
    def __init__(self) -> None:
        super().__init__(item=" ")


class HorizontalLine(Border):
    def __init__(self) -> None:
        super().__init__(item="━")


class VerticalLine(Border):
    def __init__(self) -> None:
        super().__init__(item="┃\n", measure="height")


class Connector1(Border):
    def __init__(self) -> None:
        super().__init__(item="┏")

    def render(self) -> RenderableType:
        width = self.size.width - 1
        height = self.size.height - 1
        if width:
            self.item += "━" * width
        if height:
            self.item += "\n┃" * height

        style = "bold " if self.highlight else "dim "
        return Text(self.item, style=style + self.color)


class Connector2(Border):
    def __init__(self) -> None:
        super().__init__(item="┓")

    def render(self) -> RenderableType:
        width = self.size.width - 2
        height = self.size.height - 1
        if width:
            self.item = "━" * width + self.item
        if height:
            self.item += "\n┃" * height

        style = "bold " if self.highlight else "dim "
        return Text(self.item, style=style + self.color)


class Connector3(Border):
    def __init__(self) -> None:
        super().__init__(item="┗")

    def render(self) -> RenderableType:
        width = self.size.width - 1
        height = self.size.height - 1
        if width:
            self.item += "━" * width
        if height:
            self.item += "\n┃" * height

        style = "bold " if self.highlight else "dim "
        return Text(self.item, style=style + self.color)


class Connector4(Border):
    def __init__(self) -> None:
        super().__init__(item="┛")

    def render(self) -> RenderableType:
        width = self.size.width - 2
        height = self.size.height - 1
        if width:
            self.item = "━" * width + self.item
        if height:
            self.item += "\n┃" * height

        style = "bold " if self.highlight else "dim "
        return Text(self.item, style=style + self.color)
