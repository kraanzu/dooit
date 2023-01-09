from typing import List
from rich.console import RenderableType
from rich.markup import render
from rich.text import Text, TextType
from rich.table import Table
from textual.widget import Widget

from ...utils.conf_reader import Config
from ..events import StatusType

bar = Config().get("bar")


class StatusBar(Widget):
    """
    A status bar widget for showing messages and looks :)
    """

    def __init__(self) -> None:
        super().__init__()
        self.message = Text()
        self.status = "NORMAL"
        self.color = "blue"
        self.set_interval(1, self.refresh)

    def set_message(self, message: TextType = "") -> None:
        self.message = message
        self.refresh()

    def clear_message(self) -> None:
        self.set_message()

    def set_status(self, status: StatusType) -> None:
        self.status = status

        if status == "NORMAL":
            self.color = "blue"
        elif status == "INSERT":
            self.color = "blue"
        elif status == "DATE":
            self.color = "blue"
        elif status == "SEARCH":
            self.color = "blue"
        elif status == "SORT":
            self.color = "blue"

        self.refresh()

    def render(self) -> RenderableType:

        renderable = Text()

        d = {
            "status": self.status,
            "message": self.message,
        }
        expandables = 0
        width = self.size.width

        renderables, kwargs = zip(*[widget.render() for widget in bar])

        row: List[Text] = []
        for i, attrs in zip(renderables, kwargs):
            if isinstance(i, Text):
                i = i.markup

            i = str(i)
            i = i.format(**d)
            i = Text.from_markup(i)
            row.append(i)

            if "ratio" in attrs:
                expandables += 1
            else:
                w = attrs["width"] = attrs.get("width", None) or len(i)
                width -= w

        for attrs in kwargs:
            if "ratio" in attrs:
                attrs["width"] = width // expandables

        for i, j in zip(row, kwargs):
            justify = j["justify"]
            width = j["width"] - len(i)

            if justify == "right":
                i.pad_left(width)
            elif justify == "left":
                i.pad_right(width)
            elif justify == "center":
                i.pad(width // 2)

            renderable += i

        return renderable
