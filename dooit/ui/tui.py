from textual.app import App
from ..ui.widgets.status_bar import StatusBar
from ..ui.widgets import NavBar, TodoList
from ..api import manager


class Dooit(App):
    async def on_mount(self):
        self.navbar = NavBar()
        self.todos = TodoList()
        self.bar = StatusBar()

        await self.view.dock(self.bar, edge="bottom", size=1)
        await self.view.dock(self.navbar, size=20, edge="left")
        await self.view.dock(self.todos)

    async def action_quit(self) -> None:
        manager.export()
        return await super().action_quit()
