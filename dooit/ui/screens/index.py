from textual import events, on, work
from textual.containers import Container
from dooit.api.manager import manager
from dooit.ui.widgets.empty import EmptyWidget
from dooit.ui.widgets.bar import Searcher
from dooit.ui.events import (
    TopicSelect,
    SwitchTab,
    Notify,
    ChangeStatus,
    SpawnHelp,
    CommitData,
)
from dooit.ui.widgets import WorkspaceTree, TodoTree, StatusBar
from .base import BaseScreen


class DualSplit(Container):
    pass


class DualSplitLeft(Container):
    pass


class DualSplitRight(Container):
    pass


class MainScreen(BaseScreen):
    def compose(self):
        with DualSplit():
            with DualSplitLeft():
                yield WorkspaceTree(manager)

            with DualSplitRight():
                yield EmptyWidget("dashboard")

        yield StatusBar()

    def set_message(self, message: str):
        self.query_one(StatusBar).set_message(message)

    @property
    def bar(self):
        return self.query_one(StatusBar)

    async def on_key(self, event: events.Key) -> None:
        key = self.resolve_key(event)
        if self.bar.status == "SEARCH":
            return await self.query_one(Searcher).keypress(key)

        visible_focused = [i for i in self.query(".focus") if i.display][0]
        await visible_focused.keypress(key)

    async def clear_right(self):
        try:
            self.query_one("TodoTree.current").remove_class("current")
        except Exception:
            pass

    @work(exclusive=True)
    async def mount_todos(self, model):
        with self.app.batch_update():
            await self.clear_right()
            if widgets := self.query(f"#Tree-{model.uuid}"):
                current_widget = widgets.first()
                current_widget.add_class("current")
            else:
                current_widget = TodoTree(model)
                current_widget.add_class("current")
                await self.query_one(DualSplitRight).mount(current_widget)

    async def mount_dashboard(self):
        await self.clear_right()
        await self.mount(EmptyWidget(), after=self.query_one(WorkspaceTree))

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
        try:
            visible_todo = self.query_one("TodoTree.current")
            visible_todo.toggle_class("focus")
        except Exception:
            pass

    @on(ChangeStatus)
    async def change_status(self, event: ChangeStatus):
        self.query_one(StatusBar).set_status(event.status)

    @on(SpawnHelp)
    async def spawn_help(self, _: SpawnHelp):
        self.app.push_screen("help")

    @on(Notify)
    async def notify(self, event: Notify):
        self.query_one(StatusBar).set_message(event.message)

    @on(CommitData)
    async def commit_data(self, _: CommitData):
        manager.commit()
