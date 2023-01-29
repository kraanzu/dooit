from textual.app import App
from textual import events
from dooit.utils.watcher import Watcher
from dooit.ui.events import *  # noqa
from dooit.ui.widgets import WorkspaceTree, TodoTree, StatusBar, HelpScreen
from dooit.api.manager import manager
from dooit.ui.css.screen import screen_CSS


class Dooit(App):

    CSS = screen_CSS
    SCREENS = {"help": HelpScreen(name="help")}
    BINDINGS = [("ctrl+q", "quit", "Quit App")]

    async def on_load(self):
        self.navbar = WorkspaceTree()
        self.todos = TodoTree()
        self.bar = StatusBar()

    async def on_mount(self):
        self.watcher = Watcher()
        self.current_focus = "navbar"
        self.navbar.toggle_highlight()
        self.set_interval(1, self.poll)

    async def poll(self):
        if not manager.is_locked() and self.watcher.has_modified():
            if manager.refresh_data():
                await self.navbar._refresh_data()

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
        event.sender.sort(attr=event.method)

    async def on_change_status(self, event: ChangeStatus):
        self.bar.set_status(event.status)

    async def on_notify(self, event: Notify):
        self.bar.set_message(event.message)

    async def on_spawn_help(self, event: SpawnHelp):
        self.push_screen("help")
