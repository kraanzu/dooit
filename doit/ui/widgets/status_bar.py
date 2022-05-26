from typing import Literal
from datetime import datetime
from rich.console import RenderableType
from rich.text import Text
from textual.widget import Widget


class StatusBar(Widget):
    """
    A status bar widget for showing messages and looks :)
    """

    def __init__(self):
        super().__init__()
        self.message = ""
        self.status = "NORMAL"
        self.color = "blue"
        self.set_interval(1, self.refresh)

    def set_message(self, message):
        self.message = message
        self.refresh()

    def clear_message(self):
        self.set_message("")

    def get_clock(self) -> str:
        """
        Returns current time
        """
        return f"{datetime.now().time().strftime('   %X ')}"

    def get_date(self) -> str:
        """
        Returns current time
        """
        return f"{datetime.today().strftime('   %D ')}"

    def set_status(self, status: str = Literal["NORMAL", "INSERT", "DATE", "SEARCH"]):
        self.status = status
        match status:
            case "NORMAL":
                self.color = "blue"
            case "INSERT":
                self.color = "cyan"
            case "DATE":
                self.color = "yellow"
            case "SEARCH":
                self.color = "magenta"
        self.refresh()

    def render(self) -> RenderableType:
        from rich.table import Table

        header_table = Table.grid(padding=(0, 1), expand=True)
        header_table.add_column("status", justify="center", width=len(self.status) + 1)
        header_table.add_column("message", justify="left", ratio=1)
        header_table.add_column("date", justify="center", width=13)
        header_table.add_column("clock", justify="center", width=12)

        status = Text(f" {self.status}", style=f"reverse {self.color}")
        msg = Text(f" {self.message}", style="magenta on black")
        msg.pad_right(self.size.width)

        header_table.add_row(
            status,
            msg,
            Text(
                self.get_date(),
                style="reverse green",
            ),
            Text(
                self.get_clock(),
                style="reverse yellow",
            ),
        )
        return header_table


if __name__ == "__main__":
    from textual.app import App

    class MyApp(App):
        async def on_mount(self):
            await self.view.dock(StatusBar())

    MyApp.run()
