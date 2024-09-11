from collections import defaultdict
from typing import TYPE_CHECKING, List, Callable
from dooit.ui.api.plug import PluginManager
from dooit.ui.events.events import DooitEvent, SwitchTab
from dooit.ui.registry import registry
from dooit.ui.widgets.trees.model_tree import ModelTree
from dooit.ui.widgets import BarWidget
from dooit.ui.api.components import TodoLayout, WorkspaceLayout


if TYPE_CHECKING:
    from ..tui import Dooit


class DooitAPI:
    def __init__(self, app: "Dooit") -> None:
        self.app = app
        self.plugin_manager = PluginManager()
        self.plugin_manager.scan()
        self.keybinds = defaultdict(lambda: defaultdict(lambda: lambda: None))

    def no_op(self):
        pass

    def notify(self, message: str) -> None:
        self.app.notify(message)

    def __set_key(self, mode: str, key: str, callback: Callable) -> None:
        self.keybinds[mode][key] = callback

    def set_key_normal(self, key: str, callback: Callable) -> None:
        self.__set_key("NORMAL", key, callback)

    def handle_key(self, key: str) -> None:
        self.keybinds[self.bar_mode][key]()

    def trigger_event(self, event: DooitEvent):
        event_name = event.snake_case
        for obj in self.plugin_manager.events[event_name]:
            obj(self)

    # -----------------------------------------
    @property
    def bar_mode(self) -> str:
        return self.app.mode

    @property
    def focused(self) -> ModelTree:
        focused = self.app.focused
        if isinstance(focused, ModelTree):
            return focused

        raise ValueError(f"Expected BaseTree, got {type(focused)}")

    def switch_focus(self):
        if w := self.app.focused:
            w.post_message(SwitchTab())

    def move_down(self):
        self.focused.action_cursor_down()

    def move_up(self):
        self.focused.action_cursor_up()

    def edit(self, property: str):
        self.focused.start_edit(property)

    def edit_description(self):
        return self.edit("description")

    def edit_due(self):
        return self.edit("due")

    def edit_recurrence(self):
        return self.edit("recurrence")

    def add_sibling(self):
        self.focused.create_node()

    def set_workspace_layout(self, layout: WorkspaceLayout):
        registry.set_workspace_layout(layout)
        self.app.workspace_tree.refresh_options()

    def set_todo_layout(self, layout: TodoLayout):
        registry.set_todo_layout(layout)

    def set_bar(self, widgets: List[BarWidget]):
        self.app.bar.set_widgets(widgets)
