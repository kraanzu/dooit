import webbrowser
from textual import on
from textual.app import App
from textual.message import Message
from dooit.api.manager import manager
from dooit.ui.events.events import ChangeStatus, DooitEvent, ModeType, Startup
from dooit.ui.widgets import Bar
from dooit.ui.widgets.trees.workspaces_tree import WorkspacesTree
from dooit.utils.watcher import Watcher
from dooit.ui.css.main import screen_CSS
from dooit.ui.screens import MainScreen, HelpScreen
from textual.binding import Binding
from .api import DooitAPI

PRINTABLE = (
    "0123456789"
    + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    + "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
)


class Dooit(App):
    CSS = screen_CSS
    SCREENS = {
        "main": MainScreen(name="main"),
        "help": HelpScreen(name="help"),
    }

    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit", show=False, priority=True),
        Binding("ctrl+q", "quit", "Quit", show=False, priority=True),
    ]

    def __init__(self):
        super().__init__()
        self.api = DooitAPI(self)
        self._mode: ModeType = "NORMAL"

    async def on_load(self):
        self.post_message(Startup())

    async def on_mount(self):
        self.auto_refresh = 0.1
        self.watcher = Watcher()
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
    def global_message(self, event: Message):
        self.api.trigger_event(event)

    @on(ChangeStatus)
    def change_status(self, event: ChangeStatus):
        self._mode = event.status

    async def action_quit(self) -> None:
        manager.commit()
        return await super().action_quit()

    async def action_open_url(self, url: str) -> None:
        webbrowser.open(url, new=2)


if __name__ == "__main__":
    Dooit().run()
