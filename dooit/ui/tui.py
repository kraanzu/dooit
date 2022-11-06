from typing import Union
from textual.app import App
from textual import events
from dooit.utils.watcher import Watcher
from ..ui.widgets.help_menu import HelpMenu
from ..ui.events import *  # noqa
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
        self.help_menu = HelpMenu()
        self.current_focus = "navbar"
        self.navbar.toggle_highlight()

    async def on_mount(self):
        self.set_interval(1, self.poll)
        await self.setup_grid()

    async def poll(self):
        if self.watcher.has_modified():
            nav_edit = self.navbar.editing
            manager.refresh_data()
            self.navbar._refresh_rows()
            await self.todos.update_table(self.navbar.item)
            await self.navbar._start_edit(nav_edit)

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

        await self.view.dock(self.help_menu, z=2)
        self.help_menu.visible = False

    async def action_quit(self) -> None:
        manager.commit()
        return await super().action_quit()

    def toggle_highlight(self):
        self.navbar.toggle_highlight()
        self.todos.toggle_highlight()

    async def on_key(self, event: events.Key) -> None:

        if (event.key == "?") and (
            self.bar.status == "NORMAL" or self.help_menu.visible
        ):
            self.help_menu.visible = not self.help_menu.visible
            return

        if self.navbar.has_focus:
            await self.navbar.handle_key(event)
        else:
            await self.todos.handle_key(event)

    async def handle_topic_select(self, event: TopicSelect):
        await self.todos.update_table(event.item)

    async def handle_switch_tab(self, _: SwitchTab):
        self.toggle_highlight()

    async def handle_apply_sort_method(self, event: ApplySortMethod):
        model: Union[Workspace, Todo] = event.sender
        model.sort(event.method)

    async def handle_change_status(self, event: ChangeStatus):
        self.bar.set_status(event.status)

    async def handle_notify(self, event: Notify):
        self.bar.set_message(event.message)
