from typing import Union
from textual.app import App
from textual import events
from dooit.utils.plugin_manager import Plug
from dooit.utils.watcher import Watcher
from ..ui.widgets.help_menu import HelpMenu
from ..ui.events import *  # noqa
from ..ui.widgets import NavBar, TodoList, StatusBar
from ..api.manager import manager
from ..api.workspace import Workspace
from ..api.todo import Todo
from ..ui.css.screen import screen_CSS


class Dooit(App):

    CSS = screen_CSS

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
        self.set_timer(3, self.start_plugins)

    def start_plugins(self):
        Plug.entry()

    async def poll(self):
        if self.watcher.has_modified():
            manager.refresh_data()
            await self.navbar._refresh_data()
            await self.todos.update_table(self.navbar.item)
            self.bar.set_message(str(self.navbar.current))

    def compose(self):
        yield self.navbar
        yield self.todos
        yield self.bar

    async def action_quit(self) -> None:
        manager.commit()
        return await super().action_quit()

    def toggle_highlight(self):
        self.navbar.toggle_highlight()
        self.todos.toggle_highlight()

    async def on_key(self, event: events.Key) -> None:
        # if (event.key == "?") and (
        #     self.bar.status == "NORMAL" or self.help_menu.visible
        # ):
        #     self.help_menu.visible = not self.help_menu.visible
        #     return

        if self.navbar.has_focus:
            await self.navbar.handle_key(event)
        else:
            await self.todos.handle_key(event)

    async def on_topic_select(self, event: TopicSelect):
        await self.todos.update_table(event.item)

    async def on_switch_tab(self, _: SwitchTab):
        self.toggle_highlight()

    async def on_apply_sort_method(self, event: ApplySortMethod):
        model: Union[Workspace, Todo] = event.sender
        model.sort(event.method)

    async def on_change_status(self, event: ChangeStatus):
        self.bar.set_status(event.status)

    async def on_notify(self, event: Notify):
        self.bar.set_message(event.message)
