from textual import events, on, work
from textual.containers import Container
from dooit.api.manager import manager
from dooit.ui.events.events import DateModeSwitch
from dooit.ui.widgets.empty import EmptyWidget
from dooit.ui.widgets.bar import Searcher
from dooit.ui.events import (
    TopicSelect,
    SwitchTab,
    Notify,
    ChangeStatus,
    SpawnHelp,
    CommitData,
    ApplySort,
)
from dooit.ui.widgets import WorkspaceTree, TodoTree, StatusBar
from dooit.ui.widgets.inputs import Due
from dooit.ui.widgets.tree import Tree
from .base import BaseScreen


class DualSplit(Container):
    pass


class DualSplitLeft(Container):
    pass


class DualSplitRight(Container):
    pass


class MainScreen(BaseScreen):
    date_style = "classic"

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
        event.prevent_default()
        event.stop()

        key = self.resolve_key(event)
        await self.send_keypress(key)

    async def send_keypress(self, key: str):
        if self.bar.status == "SEARCH":
            return await self.query_one(Searcher).keypress(key)

        visible_focused = [i for i in self.query(".focus") if i.display][0]
        await visible_focused.keypress(key)

    async def clear_right(self) -> None:
        try:
            self.query_one("TodoTree.current").remove_class("current")
        except Exception:
            pass

    @work(exclusive=True)
    async def mount_todos(self, model) -> None:
        with self.app.batch_update():
            await self.clear_right()
            if widgets := self.query(f"#Tree-{model.uuid}"):
                current_widget = widgets.first()
                current_widget.add_class("current")
            else:
                current_widget = TodoTree(model)
                current_widget.add_class("current")
                await self.query_one(DualSplitRight).mount(current_widget)

    async def mount_dashboard(self) -> None:
        await self.clear_right()
        await self.mount(EmptyWidget(), after=self.query_one(WorkspaceTree))

    @on(events.Paste)
    async def paste_texts(self, event: events.Paste) -> None:
        event.prevent_default()
        event.stop()
        if not event.text:
            return
        await self.send_keypress(f"events.Paste:{event.text}")

    @on(ApplySort)
    async def apply_sort(self, event: ApplySort) -> None:
        await self.query_one(event.query, expect_type=Tree).apply_sort(
            event.widget_id, event.method
        )

    @on(TopicSelect)
    async def topic_select(self, event: TopicSelect) -> None:
        event.stop()
        if model := event.model:
            self.mount_todos(model)
        else:
            await self.mount_dashboard()

    @on(SwitchTab)
    async def switch_tab(self, _: SwitchTab) -> None:
        self.query_one(WorkspaceTree).toggle_class("focus")
        try:
            visible_todo = self.query_one("TodoTree.current")
            visible_todo.toggle_class("focus")
        except Exception:
            pass

    @on(ChangeStatus)
    async def change_status(self, event: ChangeStatus) -> None:
        self.query_one(StatusBar).set_status(event.status)

    @on(SpawnHelp)
    async def spawn_help(self, _: SpawnHelp) -> None:
        self.app.push_screen("help")

    @on(Notify)
    async def notify(self, event: Notify) -> None:
        self.query_one(StatusBar).set_message(event.message)

    @on(DateModeSwitch)
    async def date_mode_switch(self, _: DateModeSwitch) -> None:
        self.date_style = "classic" if self.date_style != "classic" else "remaining"
        [i.refresh() for i in self.query(Due)]

    @on(CommitData)
    async def commit_data(self, _: CommitData) -> None:
        manager.commit()
