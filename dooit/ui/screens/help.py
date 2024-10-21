from rich.console import RenderableType
from rich.style import Style
from rich.table import Table
from rich.text import Text
from textual.app import ComposeResult
from textual.widgets import Static

from dooit.ui.api import KeyBindType
from .base import BaseScreen


class HelpWidget(Static):
    DEFAULT_CSS = """
    HelpWidget {
        content-align: center middle;
        width: 80%;
        margin: 1;
    }
    """


class Header(HelpWidget):
    def render(self) -> RenderableType:
        return "Welcome to Dooit!"


class Outro(HelpWidget):
    def render(self) -> RenderableType:
        thanks = Text.from_markup("     Thanks for using Dooit <3")
        github = Text.from_markup("You can find this project on  github -> ")
        go_back = Text.from_markup("     Use [reverse] escape [/reverse] to go back")

        github.highlight_words(
            [" github -> "],
            style=Style.from_meta(
                {"@click": "app.quit"},
            ),
        )

        return thanks + "\n" + github + "\n\n" + go_back


class DooitKeyTable(HelpWidget):
    DEFAULT_CSS = """
    DooitKeyTable {
        padding: 1 2;
    }
    """

    COMPONENT_CLASSES = {
        "keybind",
        "arrow",
        "description",
    }
    BORDER_TITLE = "Key Bindings"

    def __init__(self, keybinds: KeyBindType):
        super().__init__()
        self.keybinds = keybinds

    def render(self) -> RenderableType:
        t = Table.grid(expand=True, padding=(0, 1))

        t.add_column("key")
        t.add_column("arrow")
        t.add_column("description")
        t.title_justify = "left"

        for _, keybinds in self.keybinds.items():
            for keybind, func in keybinds.items():
                keybind = Text(keybind, style=self.get_component_rich_style("keybind"))
                arrow = Text("->", style=self.get_component_rich_style("arrow"))
                description = (
                    Text(
                        func.description,
                        style=self.get_component_rich_style("description"),
                    )
                    if func
                    else Text("")
                )

                t.add_row(keybind, arrow, description)

        return t


class HelpScreen(BaseScreen):
    """
    Help Screen to view Help Menu
    """

    DEFAULT_CSS = """
    HelpScreen {
        align: center top;
    }
    """

    BINDINGS = [
        ("escape", "app.pop_screen", "Pop screen"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield DooitKeyTable(self.api.keys.keybinds)
        yield Outro()
