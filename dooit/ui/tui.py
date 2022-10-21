from textual import events
from textual.app import App
from dooit.api.model import Model

from dooit.ui.events.events import *
from dooit.ui.widgets import navbar  # noqa
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

        await self.setup_grid()

    async def setup_grid(self):
        self.grid = await self.view.dock_grid()
        self.grid.add_column("nav", fraction=20)
        self.grid.add_column("todo", fraction=80)
        self.grid.add_row("body")
        self.grid.add_row("bar", size=1)

        self.grid.add_areas(
            navbar="nav,body",
            todos="todo,body",
            bar="nav-start|todo-end,bar",
        )

        self.grid.place(
            navbar=self.navbar,
            todos=self.todos,
            bar=self.bar,
        )

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

    async def handle_apply_sort_method(self, event: ApplySortMethod):
        model: Model = event.sender
        model.sort(event.method)
