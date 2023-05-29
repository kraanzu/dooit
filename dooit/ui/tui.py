from functools import partial
from textual.app import App
from textual import events, on
from dooit.ui.widgets.empty import EmptyWidget
from dooit.utils.watcher import Watcher
from dooit.ui.events import (
    TopicSelect,
    SwitchTab,
    Notify,
    ChangeStatus,
    SpawnHelp,
    CommitData,
    ExitApp,
)
from dooit.ui.widgets import WorkspaceTree, TodoTree, StatusBar
from dooit.api.manager import manager
from dooit.ui.css.main import screen_CSS
from dooit.ui.screens import HelpScreen

PRINTABLE = (
    "0123456789"
    + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    + "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
)


class Dooit(App):
    CSS = screen_CSS
    SCREENS = {
        "help": HelpScreen(name="help"),
    }

    async def on_mount(self):
        self.watcher = Watcher()
        self.x = 1
        self.set_interval(1, self.poll)

    async def poll(self):
        # TODO: implement auto refresh for modified data

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

    def compose(self):
        yield WorkspaceTree(manager)
        yield EmptyWidget("dashboard")
        yield StatusBar()

    async def action_quit(self) -> None:
        manager.commit()
        return await super().action_quit()

    async def on_key(self, event: events.Key) -> None:
        key = (
            event.character
            if (event.character and (event.character in PRINTABLE))
            else event.key
        )
        if self.screen.name != "help":
            await self.query_one(".focus").keypress(key)

    async def on_topic_select(self, event: TopicSelect):
        event.stop()
        model = event.model
        func = partial(self.mount_todos, model)
        self.run_worker(func, exclusive=True)

    async def mount_todos(self, model):
        if widgets := self.query(EmptyWidget):
            for widget in widgets:
                await widget.remove()

        if widgets := self.query(TodoTree):
            for i in widgets:
                i.display = False

        if widgets := self.query(f"#Tree-{model.uuid}"):
            current_widget = widgets.first()
            current_widget.display = True
        else:
            current_widget = TodoTree(model)
            await self.mount(current_widget, after=self.query_one(WorkspaceTree))

    @on(SwitchTab)
    async def switch_tab(self, _: SwitchTab):
        self.query_one(WorkspaceTree).toggle_class("focus")
        visible_todo = [i for i in self.query(TodoTree) if i.display][0]
        visible_todo.toggle_class("focus")

    @on(ChangeStatus)
    async def hange_status(self, event: ChangeStatus):
        self.query_one(StatusBar).set_status(event.status)

    @on(Notify)
    async def notify(self, event: Notify):
        self.query_one(StatusBar).set_message(event.message)

    @on(SpawnHelp)
    async def spawn_help(self, _: SpawnHelp):
        self.push_screen("help")

    @on(CommitData)
    async def commit_data(self, _: CommitData):
        manager.commit()

    @on(ExitApp)
    async def exit_app(self, _: ExitApp):
        await self.action_quit()
