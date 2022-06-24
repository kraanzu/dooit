from datetime import datetime
from rich.console import RenderableType
from rich.text import Text
from rich.table import Table
from textual.widget import Widget

from ...utils.config import conf
from ..events import StatusType


class StatusBar(Widget):
    """
    A status bar widget for showing messages and looks :)
    """

    def __init__(self) -> None:
        super().__init__()
        self.message = ""
        self.status = "NORMAL"
        self.color = "blue"
        self.set_interval(1, self.refresh)
        config = conf.load_config("status_bar")
        self.theme = config["theme"]
        self.clock_icon = config["icons"]["clock"]
        self.calendar_icon = config["icons"]["calendar"]

    def set_message(self, message) -> None:
        self.message = message
        self.refresh()

    def clear_message(self) -> None:
        self.set_message("")

    def get_clock(self) -> str:
        """
        Returns current time
        """

        return f"{datetime.now().time().strftime(' {0}  %X ')}".format(self.clock_icon)

    def get_date(self) -> str:
        """
        Returns current time
        """
        return f"{datetime.today().strftime(' {0}  %D ')}".format(self.calendar_icon)

    def set_status(self, status: StatusType) -> None:
        self.status = status
        match status:
            case "NORMAL":
                self.color = self.theme["normal"]
            case "INSERT":
                self.color = self.theme["insert"]
            case "DATE":
                self.color = self.theme["date"]
            case "SEARCH":
                self.color = self.theme["search"]
            case "SORT":
                self.color = self.theme["sort"]
        self.refresh()

    def render(self) -> RenderableType:

        style_clock = self.theme["clock"]
        style_date = self.theme["date"]

        bar = Table.grid(padding=(0, 1), expand=True)
        bar.add_column("status", justify="center", width=len(self.status) + 1)
        bar.add_column("message", justify="left", ratio=1)
        bar.add_column("date", justify="center", width=13)
        bar.add_column("clock", justify="center", width=12)

        status = Text(f" {self.status}", style=f"reverse {self.color}")
        message = Text.from_markup(f" {self.message}", style="magenta on black")
        message.pad_right(self.size.width)

        bar.add_row(
            status,
            message,
            Text(
                self.get_date(),
                style=style_date,
            ),
            Text(
                self.get_clock(),
                style=style_clock,
            ),
        )
        return bar


if __name__ == "__main__":
    from textual.app import App

    class MyApp(App):
        async def on_mount(self):
            await self.view.dock(StatusBar())

    MyApp.run()
