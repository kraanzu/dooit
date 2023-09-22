import webbrowser
from textual.app import App
from dooit.api.manager import manager
from dooit.utils.watcher import Watcher
from dooit.ui.widgets import WorkspaceTree, TodoTree
from dooit.ui.css.main import screen_CSS
from dooit.ui.screens import MainScreen, HelpScreen
from textual.binding import Binding

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

    async def on_mount(self):
        self.watcher = Watcher()
        self.set_interval(1, self.poll)
        self.push_screen("main")

    async def poll(self):
        if (
            not manager.is_locked()
            and self.watcher.has_modified()
            and manager.refresh_data()
        ):
            await self.query_one(WorkspaceTree).force_refresh(manager)
            for i in self.query(TodoTree):
                index = manager._get_child_index("workspace", uuid=i.model.uuid)
                if index == -1:
                    i.remove()
                else:
                    await i.force_refresh(manager._get_children("workspace")[index])

    async def action_quit(self) -> None:
        manager.commit()
        return await super().action_quit()

    async def action_open_url(self, url: str) -> None:
        webbrowser.open(url, new=2)


if __name__ == "__main__":
    Dooit().run()
