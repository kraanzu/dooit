import webbrowser
from typing import Optional
from textual import on
from textual.app import App
from textual.binding import Binding

from dooit.api.theme import DooitThemeBase
from dooit.ui.events.events import ModeChanged, DooitEvent, ModeType, Startup
from dooit.ui.widgets import BarSwitcher
from dooit.ui.widgets.bars import StatusBar
from dooit.ui.widgets.trees import WorkspacesTree
from dooit.ui.screens import MainScreen, HelpScreen
from dooit.ui.widgets.trees.model_tree import ModelTree
from dooit.utils import CssManager
from .api import DooitAPI
from ..api import manager

PRINTABLE = (
    "0123456789"
    + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    + "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
)


class Dooit(App):
    CSS_PATH = CssManager.css_file

    SCREENS = {
        "main": MainScreen,
        "help": HelpScreen,
    }

    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit", show=False, priority=True),
        Binding("ctrl+q", "quit", "Quit", show=False, priority=True),
    ]

    def __init__(self, connection_string: Optional[str] = None):
        super().__init__()
        self.api = DooitAPI(self)
        self._mode: ModeType = "NORMAL"
        manager.register_engine(connection_string)

    async def on_load(self):
        self.post_message(Startup())
        self.post_message(ModeChanged("NORMAL"))

    async def on_mount(self):
        self.set_interval(1, self.poll)
        self.push_screen("main")

    @property
    def workspace_tree(self) -> WorkspacesTree:
        return self.query_one(WorkspacesTree)

    @property
    def bar(self) -> StatusBar:
        return self.query_one(BarSwitcher).status_bar

    @property
    def bar_switcher(self) -> BarSwitcher:
        return self.query_one(BarSwitcher)

    def get_mode(self) -> ModeType:
        return self._mode

    @property
    def current_theme(self) -> DooitThemeBase:
        return self.api.css_manager.theme

    async def poll(self):
        def refresh_all_trees():
            trees = self.query(ModelTree)
            for tree in trees:
                tree.force_refresh()

        if manager.has_changed():
            refresh_all_trees()

    @on(DooitEvent)
    def global_message(self, event: DooitEvent):
        if isinstance(self.screen, MainScreen):
            self.api.trigger_event(event)
            self.bar.trigger_event(event)

    @on(ModeChanged)
    def change_status(self, event: ModeChanged):
        self._mode = event.mode

    async def action_open_url(self, url: str) -> None:
        webbrowser.open(url, new=2)


if __name__ == "__main__":
    Dooit().run()
