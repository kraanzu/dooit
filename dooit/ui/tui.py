import webbrowser
from textual import on
from textual.app import App
from textual.message import Message
from dooit.api.manager import manager
from dooit.ui.events.events import DooitEvent, Startup
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

    async def poll(self):
        return
        # if (
        #     not manager.is_locked()
        #     and self.watcher.has_modified()
        #     and manager.refresh_data()
        # ):
        #     await self.query_one(WorkspaceTree).force_refresh(manager)
        #     for i in self.query(TodoTree):
        #         index = manager._get_child_index("workspace", uuid=i.model.uuid)
        #         if index == -1:
        #             i.remove()
        #         else:
        #             await i.force_refresh(manager._get_children("workspace")[index])

    @on(DooitEvent)
    def global_message(self, event: Message):
        self.api.trigger_event(event)

    async def action_quit(self) -> None:
        manager.commit()
        return await super().action_quit()

    async def action_open_url(self, url: str) -> None:
        webbrowser.open(url, new=2)


if __name__ == "__main__":
    Dooit().run()
