from typing import Union
from textual.app import App
from textual import events

from dooit.utils.watcher import Watcher
from ..ui.events import *
from ..ui.widgets import NavBar, TodoList, StatusBar
from ..api.manager import manager
from ..api.workspace import Workspace
from ..api.todo import Todo


class Dooit(App):
    async def on_load(self):
        self.navbar = NavBar()
        self.todos = TodoList()
        self.bar = StatusBar()
        self.watcher = Watcher()
        self.current_focus = "navbar"
        self.navbar.toggle_highlight()

    async def on_mount(self):
        self.set_interval(1, self.poll)
        await self.setup_grid()

    async def poll(self):
        if self.watcher.has_modified():
            manager.refresh_data()
            self.navbar._refresh_rows()
            if item := self.navbar.item:
                self.todos.update_table(item)
            self.bar.set_message('updated!')

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
        model: Union[Workspace, Todo] = event.sender
        model.sort(event.method)

    async def handle_change_status(self, event: ChangeStatus):
        self.bar.set_status(event.status)

    async def handle_notify(self, event: Notify):
        self.bar.set_message(event.message)
