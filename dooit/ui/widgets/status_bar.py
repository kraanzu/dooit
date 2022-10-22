from rich.console import RenderableType
from rich.text import Text
from rich.table import Table
from textual.widget import Widget

from dooit.utils import default_config
from ...utils.config import conf
from ..events import StatusType

bar = default_config.bar


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

    def set_message(self, message) -> None:
        self.message = message
        self.refresh()

    def clear_message(self) -> None:
        self.set_message("")

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

        table = Table.grid(padding=(0, 0), expand=True)
        d = {"status": self.status, "message": self.message}
        renderables, kwargs = zip(*[widget.render() for widget in bar])

        row = []
        for i in renderables:
            if isinstance(i, Text):
                row.append(i)
            else:
                row.append(Text(str(i)))

            row[-1].plain = row[-1].plain.format(**d)

        [table.add_column(**i) for i in kwargs]
        table.add_row(*row)

        return table


if __name__ == "__main__":
    from textual.app import App

    class MyApp(App):
        async def on_mount(self):
            await self.view.dock(StatusBar())

    MyApp.run()
