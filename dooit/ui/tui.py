from textual.app import App
from textual import events, on, work
from dooit.ui.widgets.empty import EmptyWidget
from dooit.ui.widgets.bar import Searcher
from dooit.ui.widgets.tree import Tree
from dooit.utils.watcher import Watcher
from dooit.ui.events import (
    TopicSelect,
    SwitchTab,
    Notify,
    ChangeStatus,
    SpawnHelp,
    CommitData,
    StopSearch,
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

    def set_message(self, message: str):
        self.query_one(StatusBar).set_message(message)

    async def on_key(self, event: events.Key) -> None:
        key = (
            event.character
            if (event.character and (event.character in PRINTABLE))
            else event.key
        )

        if self.bar.status == "SEARCH":
            return await self.query_one(Searcher).keypress(key)

        if self.screen.name != "help":
            visible_focused = [i for i in self.query(".focus") if i.display][0]
            await visible_focused.keypress(key)

    async def clear_right(self):
        for i in self.query(TodoTree):
            i.display = False
            i.remove_class("current")

        for i in self.query(EmptyWidget):
            if not isinstance(i.parent, Tree):
                i.remove()

    @work(exclusive=True)
    async def mount_todos(self, model):
        with self.batch_update():
            await self.clear_right()
            if widgets := self.query(f"#Tree-{model.uuid}"):
                current_widget = widgets.first()
                current_widget.display = True
                current_widget.add_class("current")
            else:
                current_widget = TodoTree(model)
                current_widget.add_class("current")
                await self.mount(current_widget, after=self.query_one(WorkspaceTree))

    async def mount_dashboard(self):
        await self.clear_right()
        await self.mount(EmptyWidget(), after=self.query_one(WorkspaceTree))

    @property
    def bar(self):
        return self.query_one(StatusBar)

    @on(TopicSelect)
    async def topic_select(self, event: TopicSelect):
        event.stop()
        if model := event.model:
            self.mount_todos(model)
        else:
            await self.mount_dashboard()

    @on(SwitchTab)
    async def switch_tab(self, _: SwitchTab):
        self.query_one(WorkspaceTree).toggle_class("focus")
        visible_todo = [i for i in self.query(TodoTree) if i.display][0]
        visible_todo.toggle_class("focus")

    @on(ChangeStatus)
    async def change_status(self, event: ChangeStatus):
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


if __name__ == "__main__":
    Dooit().run()
