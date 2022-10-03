from textual import events
from textual.app import App
from ..ui.widgets.status_bar import StatusBar
from ..ui.widgets import NavBar, TodoList
from ..api import manager


class Dooit(App):
    async def on_mount(self):
        self.navbar = NavBar()
        self.todos = TodoList()
        self.bar = StatusBar()
        self.current_focus = "navbar"

        self.navbar.highlight()
        await self.view.dock(self.bar, edge="bottom", size=1)
        await self.view.dock(self.navbar, size=30, edge="left")
        await self.view.dock(self.todos)

    async def action_quit(self) -> None:
        manager.commit()
        return await super().action_quit()

    async def on_key(self, event: events.Key) -> None:
        if self.current_focus == "navbar":
            await self.navbar.handle_key(event)
        else:
            await self.todos.handle_key(event)
