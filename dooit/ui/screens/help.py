from textual.app import ComposeResult
from textual.widgets import Static
from textual import events
from dooit.ui.widgets.help_menu import HelpMenu
from .base import BaseScreen

PRINTABLE = (
    "0123456789"
    + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    + "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
)


class HelpScreen(BaseScreen):
    """
    Help Screen to view Help Menu
    """

    BINDINGS = [
        ("escape", "app.pop_screen", "Pop screen"),
        ("question_mark", "app.pop_screen", "Pop screen"),
    ]

    def compose(self) -> ComposeResult:
        for i in HelpMenu().items():
            yield Static(i)

    async def on_key(self, event: events.Key):
        key = self.resolve_key(event)
        if key in ["j", "down"]:
            self.scroll_down()
        elif key in ["k", "up"]:
            self.scroll_up()
        elif key in ["home", "g"]:
            self.scroll_home()
        elif key in ["end", "G"]:
            self.scroll_end()
