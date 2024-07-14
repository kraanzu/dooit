from collections import defaultdict
from collections.abc import Callable
from typing import TYPE_CHECKING
from textual.message import Message
from dooit.ui.api.plug import PluginManager
from dooit.ui.widgets.trees.model_tree import ModelTree


if TYPE_CHECKING:
    from ..tui import Dooit


def camel_to_snake(name: str) -> str:
    return "".join(["_" + i.lower() if i.isupper() else i for i in name]).lstrip("_")


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

    def trigger_event(self, event: Message):
        event_name = camel_to_snake(event.__class__.__name__)
        for obj in self.plugin_manager.events[event_name]:
            obj(self)

    # -----------------------------------------
    @property
    def bar_mode(self) -> str:
        return self.app.bar.status

    @property
    def focused(self) -> ModelTree:
        focused = self.app.focused
        if isinstance(focused, ModelTree):
            return focused

        raise ValueError(f"Expected BaseTree, got {type(focused)}")

    def switch_focus(self):
        self.app.action_focus_next()
        self.app.action_focus_next()

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
