from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Static
from textual import events
from dooit.ui.widgets.help_menu import HelpMenu


class HelpScreen(Screen):
    """
    Help Screen to view Help Menu
    """

    BINDINGS = [
        ("escape", "app.pop_screen", "Pop screen"),
        ("question_mark", "app.pop_screen", "Pop screen"),
    ]
    # view = Vertical(*[Static(i) for i in HelpMenu().items()])

    def compose(self):
        for i in HelpMenu().items():
            yield Static(i)

    async def on_key(self, event: events.Key):
        key = event.character
        if key in ["j", "down"]:
            self.scroll_down()
        elif key in ["k", "up"]:
            self.scroll_up()
        elif key in ["home", "g"]:
            self.scroll_home()
        elif key in ["end", "G"]:
            self.scroll_end()
