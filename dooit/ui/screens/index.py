from textual import events, on, work
from textual.containers import Container
from textual.widgets import ContentSwitcher
from dooit.api.workspace import Workspace
from dooit.ui.events.events import ModeChanged, ShowConfirm, StartSearch
from dooit.ui.widgets.empty import WORKSPACE_EMPTY_WIDGETS, TODO_EMPTY_WIDGETS
from dooit.ui.events import (
    TopicSelect,
    SwitchTab,
    SpawnHelp,
)
from dooit.ui.widgets.trees import WorkspacesTree, TodosTree
from dooit.ui.widgets import BarSwitcher
from .base import BaseScreen


class DualSplit(Container):
    DEFAULT_CSS = """
    DualSplit {
        layout: grid;
        grid-size: 2 1;
        grid-columns: 2fr 8fr;
    }
    """


class DualSplitLeft(Container):
    pass


class DualSplitRight(Container):
    pass


class MainScreen(BaseScreen):
    DEFAULT_CSS = """
    MainScreen {
        layout: grid;
        grid-size: 1 2;
        grid-rows: 1fr 1;
    }
    """

    def compose(self):
        workspaces_tree = WorkspacesTree(Workspace._get_or_create_root())

        with DualSplit():
            with ContentSwitcher(id="workspace_switcher", initial=workspaces_tree.id):
                yield from WORKSPACE_EMPTY_WIDGETS
                yield workspaces_tree

            with ContentSwitcher(initial=TODO_EMPTY_WIDGETS[0].id, id="todo_switcher"):
                yield from TODO_EMPTY_WIDGETS

        yield BarSwitcher()

    async def handle_key(self, event: events.Key) -> bool:

        if self.app.bar_switcher.is_focused:
            return await self.app.bar_switcher.handle_key(event)

        return await super().handle_key(event)

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
            await self.mount_todos(model)
        else:
            await self.mount_dashboard()

    @on(SwitchTab)
    def switch_tab(self, event: SwitchTab) -> None:
        event.stop()

        self.query_one(WorkspacesTree).toggle_class("focus")
        try:
            visible_todo = self.query_one("TodoTree.current")
            visible_todo.toggle_class("focus")
        except Exception:
            pass

    @on(SpawnHelp)
    async def spawn_help(self, _: SpawnHelp) -> None:
        self.app.push_screen("help")

    @on(StartSearch)
    def start_search(self, event: StartSearch):
        self.app.bar_switcher.switch_to_search(event.callback)
        self.post_message(ModeChanged("SEARCH"))

    @on(ShowConfirm)
    def show_confirm(self, event: ShowConfirm):
        self.app.bar_switcher.switch_to_confirm(event.callback)
        self.post_message(ModeChanged("CONFIRM"))
