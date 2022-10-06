from textual import events
from textual.app import App
from ..api.workspace import Workspace

from dooit.ui.events.events import * #noqa
from ..ui.widgets.status_bar import StatusBar
from ..ui.widgets import NavBar, TodoList
from ..api.manager import manager


class Dooit(App):
    async def on_mount(self):
        self.navbar = NavBar()
        self.todos = TodoList()
        self.bar = StatusBar()
        self.current_focus = "navbar"

        self.navbar.toggle_highlight()
        await self.view.dock(self.bar, edge="bottom", size=1)
        await self.view.dock(self.navbar, size=25, edge="left")
        await self.view.dock(self.todos)

    async def action_quit(self) -> None:
        manager.commit()
        return await super().action_quit()

    def toggle_highlight(self):
        self.navbar.toggle_highlight()
        self.todos.toggle_highlight()

    async def on_key(self, event: events.Key) -> None:

        if self.navbar.has_focus:
            await self.navbar.handle_key(event)
        else:
            await self.todos.handle_key(event)

    async def handle_topic_select(self, event: TopicSelect):
        self.todos.update_table(event.item)

    async def handle_switch_tab(self, _: SwitchTab):
        self.toggle_highlight()

