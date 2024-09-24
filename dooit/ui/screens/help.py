from rich.console import RenderableType
from textual.app import ComposeResult
from textual.widgets import DataTable, Static
from .base import BaseScreen


class Header(Static):
    DEFAULT_CSS = """
    Header {
        content-align: center middle;
        width: 80%;
        margin: 3;
    }
    """

    def render(self) -> RenderableType:
        return "Dooit's Keybindings"


class Outro(Static):
    DEFAULT_CSS = """
    Outro {
        content-align: center middle;
        width: 80%;
    }
    """

    def render(self) -> RenderableType:
        return "Thanks for using Dooit <3"


class HelpScreen(BaseScreen):
    """
    Help Screen to view Help Menu
    """

    DEFAULT_CSS = """
    HelpScreen {
        align: center middle;
    }

    DataTable {
        content-align: center middle;
        width: 80%;
    }
    """

    BINDINGS = [
        ("escape", "app.pop_screen", "Pop screen"),
    ]

    @property
    def table(self) -> DataTable:
        return self.query_one(DataTable)

    def on_mount(self):
        self.table.add_column("key")
        self.table.add_column("description")

        self.fill_table()

    def fill_table(self):
        api = self.app.api
        keybindings = api.keybinds["NORMAL"]

        for key, func in keybindings.items():
            row = [key, func.__doc__ or "Example Func"]
            self.table.add_row(*row, height=None)

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable(cursor_type="row")
        yield Outro()
