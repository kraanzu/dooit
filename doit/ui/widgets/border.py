from rich.console import RenderableType
from rich.text import Text
from textual.widget import Widget


class Border(Widget):
    def __init__(
        self, name: str | None = None, color: str = "green", item="", measure="width"
    ) -> None:
        super().__init__(name)
        self.highlight = False
        self.color = color
        self.item = item
        self.measure = measure

    def render(self) -> RenderableType:

        count = self.size.width if self.measure == "width" else self.size.height
        style = "bold " if self.highlight else "dim "
        return Text(self.item * count, style=style + self.color)


class HorizontalLine(Border):
    def __init__(self, name: str | None = None, color: str = "green") -> None:
        super().__init__(name, color, "━")


class VerticalLine(Border):
    def __init__(
        self, name: str | None = None, color: str = "green", measure="height"
    ) -> None:
        super().__init__(name, color, "┃\n", measure)


class Connector1(Border):
    def __init__(self, name: str | None = None, color: str = "green") -> None:
        super().__init__(name, color, "┏━━")


class Connector2(Border):
    def __init__(self, name: str | None = None, color: str = "green") -> None:
        super().__init__(name, color, "┓\n┃\n┃\n")


class Connector3(Border):
    def __init__(self, name: str | None = None, color: str = "green") -> None:
        super().__init__(name, color, "┗━━")


class Connector4(Border):
    def __init__(self, name: str | None = None, color: str = "green") -> None:
        super().__init__(name, color, "┛")
