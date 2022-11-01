from rich.console import RenderableType
from rich.text import Text, TextType
from rich.table import Table
from textual.widget import Widget

from dooit.utils import default_config
from ..events import StatusType

bar = default_config.bar


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

        table = Table.grid(padding=(0, 0), expand=True)
        d = {"status": self.status, "message": self.message}
        renderables, kwargs = zip(*[widget.render() for widget in bar])

        row = []
        for i in renderables:
            if isinstance(i, Text):
                i.plain = i.plain.format(**d)
                row.append(i)
            else:
                i = str(i).format(**d)
                row.append(Text.from_markup(i))

        [table.add_column(**i) for i in kwargs]
        table.add_row(*row)

        return table


if __name__ == "__main__":
    from textual.app import App

    class MyApp(App):
        async def on_mount(self):
            await self.view.dock(StatusBar())

    MyApp.run()
