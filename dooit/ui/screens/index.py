from textual import events, on, work
from dooit.api.manager import manager
from dooit.ui.widgets.empty import EmptyWidget
from dooit.ui.widgets.bar import Searcher
from dooit.ui.widgets.tree import Tree
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


class MainScreen(BaseScreen):
    def compose(self):
        yield WorkspaceTree(manager)
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
        for i in self.query(TodoTree):
            i.display = False
            i.remove_class("current")

        for i in self.query(EmptyWidget):
            if not isinstance(i.parent, Tree):
                i.remove()

    @work(exclusive=True, thread=True)
    async def mount_todos(self, model):
        with self.app.batch_update():
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

    @on(SpawnHelp)
    async def spawn_help(self, _: SpawnHelp):
        self.app.push_screen("help")

    @on(Notify)
    async def notify(self, event: Notify):
        self.query_one(StatusBar).set_message(event.message)

    @on(CommitData)
    async def commit_data(self, _: CommitData):
        manager.commit()
