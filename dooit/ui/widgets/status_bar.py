from inspect import getfullargspec as get_args
from typing import Callable
from rich.console import RenderableType
from rich.table import Table
from rich.text import Text, TextType
from textual.widget import Widget
from dooit.utils.conf_reader import Config
from dooit.api import manager
from ..events import StatusType

bar = Config().get("bar")


class StatusBar(Widget):
    """
    A status bar widget for showing messages and looks :)
    """

    def __init__(self) -> None:
        super().__init__()
        self.message = ""
        self.status = "NORMAL"
        self.set_interval(1, self.refresh)

    def set_message(self, message: TextType = "") -> None:

        if isinstance(message, Text):
            message = message.markup

        self.message = message
        self.refresh()

    def clear_message(self) -> None:
        self.set_message()

    def set_status(self, status: StatusType) -> None:
        self.status = status
        self.refresh()

    def get_params(self):
        return {
            "status": self.status,
            "message": self.message,
            "manager": manager,
        }

    def render(self) -> RenderableType:

        table = Table.grid(expand=True, padding=(0, 0))
        table.add_column("A")
        table.add_column("B", ratio=1)
        table.add_column("C")

        params = self.get_params()
        renderables = []

        for col in "ABC":
            temp = Text()
            for func in bar[col]:
                if isinstance(func, Callable):
                    args = get_args(func).args
                    text = func(**{i: params[i] for i in args})
                else:
                    text = func

                if isinstance(text, Text):
                    temp += text
                else:
                    temp += Text.from_markup(str(text))

            renderables.append(temp)

        table.add_row(*renderables)
        return table
