from typing import Union
from textual.app import App
from textual import events
from dooit.utils.watcher import Watcher
from dooit.ui.widgets.help_menu import HelpScreen
from dooit.ui.events import *  # noqa
from dooit.ui.widgets import NavBar, TodoList, StatusBar
from dooit.api.manager import manager
from dooit.api.workspace import Workspace
from dooit.api.todo import Todo
from dooit.ui.css.screen import screen_CSS


class Dooit(App):

    CSS = screen_CSS
    SCREENS = {"help": HelpScreen(name="help")}
    BINDINGS = [("ctrl+q", "quit", "Quit App")]

    async def on_load(self):
        self.navbar = NavBar()
        self.todos = TodoList()
        self.bar = StatusBar()
        self.watcher = Watcher()
        self.current_focus = "navbar"
        self.navbar.toggle_highlight()

    async def on_mount(self):
        self.set_interval(1, self.poll)

    async def poll(self):
        if not manager.is_locked() and self.watcher.has_modified():
            if manager.refresh_data():
                await self.navbar._refresh_data()
                await self.todos.update_table(self.navbar.item)

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

    async def on_spawn_help(self, event: SpawnHelp):
        self.push_screen("help")
