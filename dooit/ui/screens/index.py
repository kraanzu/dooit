from textual import events, on, work
from textual.containers import Container
from dooit.api.manager import manager
from dooit.ui.widgets.empty import WORKSPACE_EMPTY_WIDGETS, TODO_EMPTY_WIDGETS
from dooit.ui.events import (
    TopicSelect,
    SwitchTab,
    ChangeStatus,
    SpawnHelp,
    CommitData,
)
from dooit.ui.widgets.switcher import FlexibleSwitcher
from dooit.ui.widgets.trees import WorkspacesTree, TodosTree
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
            workspaces_tree = WorkspacesTree(manager)
            initial = (
                workspaces_tree.id
                if manager.workspaces
                else WORKSPACE_EMPTY_WIDGETS[0].id
            )

            with FlexibleSwitcher(initial=initial, id="workspace_switcher"):
                yield from WORKSPACE_EMPTY_WIDGETS
                yield workspaces_tree

            with FlexibleSwitcher(initial=TODO_EMPTY_WIDGETS[0].id, id="todo_switcher"):
                yield from TODO_EMPTY_WIDGETS

    async def send_keypress(self, key: str):
        pass

        # visible_focused = [i for i in self.query(".focus") if i.display][0]
        # await visible_focused.keypress(key)

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
                current_widget = TodosTree(model)
                current_widget.add_class("current")
                await self.query_one(DualSplitRight).mount(current_widget)

    async def mount_dashboard(self) -> None:
        await self.clear_right()

    @on(events.Paste)
    async def paste_texts(self, event: events.Paste) -> None:
        event.prevent_default()
        event.stop()
        if not event.text:
            return
        await self.send_keypress(f"events.Paste:{event.text}")

    @on(TopicSelect)
    async def topic_select(self, event: TopicSelect) -> None:
        event.stop()
        if model := event.model:
            self.mount_todos(model)
        else:
            await self.mount_dashboard()

    @on(SwitchTab)
    async def switch_tab(self, _: SwitchTab) -> None:
        self.query_one(WorkspacesTree).toggle_class("focus")
        try:
            visible_todo = self.query_one("TodoTree.current")
            visible_todo.toggle_class("focus")
        except Exception:
            pass

    @on(SpawnHelp)
    async def spawn_help(self, _: SpawnHelp) -> None:
        self.app.push_screen("help")

    @on(CommitData)
    async def commit_data(self, _: CommitData) -> None:
        manager.commit()
