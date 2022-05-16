from rich.console import RenderableType
from rich.text import Text
from textual.widget import Widget


class Border(Widget):
    highlight = False

    def __init__(self, name: str | None = None, color: str = "green", item="") -> None:
        super().__init__(name)
        self.color = color
        self.item = item

    def render(self) -> RenderableType:
        style = "bold " if self.highlight else "dim "
        return Text(self.item * 1000, style=style + self.color)


class HorizontalLine(Border):
    def __init__(self, name: str | None = None, color: str = "green") -> None:
        super().__init__(name, color, "━")

class VerticalLine(Border):
    def __init__(self, name: str | None = None, color: str = "green") -> None:
        super().__init__(name, color, "┃\n")

class Connector1(Border):
    def __init__(self, name: str | None = None, color: str = "green") -> None:
        super().__init__(name, color, "┏")

class Connector2(Border):
    def __init__(self, name: str | None = None, color: str = "green") -> None:
        super().__init__(name, color, "┓")

class Connector3(Border):
    def __init__(self, name: str | None = None, color: str = "green") -> None:
        super().__init__(name, color, "┗")

class Connector4(Border):
    def __init__(self, name: str | None = None, color: str = "green") -> None:
        super().__init__(name, color, "┛")

