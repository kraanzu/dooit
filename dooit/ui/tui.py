import webbrowser
from textual import on
from textual.app import App
from dooit.api.manager import manager
from dooit.ui.events.events import ModeChanged, DooitEvent, ModeType, Startup
from dooit.ui.widgets import Bar
from dooit.ui.widgets.trees.workspaces_tree import WorkspacesTree
from dooit.ui.screens import MainScreen, HelpScreen
from textual.binding import Binding
from .api import DooitAPI
from .css.main import screen_CSS

PRINTABLE = (
    "0123456789"
    + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    + "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
)


class Dooit(App):
    CSS = screen_CSS
    SCREENS = {
        "main": MainScreen,
        "help": HelpScreen,
    }

    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit", show=False, priority=True),
        Binding("ctrl+q", "quit", "Quit", show=False, priority=True),
    ]

    def __init__(self):
        super().__init__()
        self.api = DooitAPI(self)
        self._mode: ModeType = "NORMAL"
        manager.register_engine()

    async def on_load(self):
        self.post_message(Startup())

    async def on_mount(self):
        self.set_interval(1, self.poll)
        self.push_screen("main")

    @property
    def workspace_tree(self) -> WorkspacesTree:
        return self.query_one(WorkspacesTree)

    @property
    def bar(self) -> Bar:
        return self.query_one(Bar)

    @property
    def mode(self) -> ModeType:
        return self._mode

    async def poll(self):
        return

    @on(DooitEvent)
    def global_message(self, event: DooitEvent):
        self.api.trigger_event(event)
        self.bar.trigger_event(event)

    @on(ModeChanged)
    def change_status(self, event: ModeChanged):
        self._mode = event.status

    async def action_open_url(self, url: str) -> None:
        webbrowser.open(url, new=2)


if __name__ == "__main__":
    Dooit().run()
