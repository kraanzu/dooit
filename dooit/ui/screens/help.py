from rich.console import RenderableType
from rich.table import Table
from textual.app import ComposeResult
from textual.widgets import Static

from dooit.ui.api.dooit_api import KeyBindType
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


class DooitKeyTable(Static):
    DEFAULT_CSS = """
    DooitKeyTable {
        content-align: center middle;
        width: 80%;
    }
    """

    def __init__(self, keybinds: KeyBindType):
        super().__init__()
        self.keybinds = keybinds

    def render(self) -> RenderableType:
        t = Table.grid(expand=True)

        t.add_column("key", width=10)
        t.add_column("description", ratio=1)

        for mode, keybinds in self.keybinds.items():
            for index, (key, func) in enumerate(keybinds.items()):
                t.add_row(key, func.__doc__ or "Example function")

        return t


class HelpScreen(BaseScreen):
    """
    Help Screen to view Help Menu
    """

    DEFAULT_CSS = """
    HelpScreen {
        align: center middle;
    }
    """

    BINDINGS = [
        ("escape", "app.pop_screen", "Pop screen"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield DooitKeyTable(self.api.keybinds)
        yield Outro()
