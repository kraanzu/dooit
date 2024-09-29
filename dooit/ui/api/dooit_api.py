from typing import TYPE_CHECKING, List

from dooit.ui.api.plug import PluginManager
from dooit.ui.events.events import DooitEvent, SwitchTab
from dooit.ui.widgets import ModelTree
from dooit.ui.widgets.bars import StatusBarWidget
from dooit.utils import CssManager

from .api_components import KeyManager, LayoutManager, Formatter

if TYPE_CHECKING:  # pragma: no cover
    from ..tui import Dooit


class DooitAPI:
    def __init__(self, app: "Dooit") -> None:
        self.app = app
        self.plugin_manager = PluginManager()
        self.plugin_manager.scan()
        self.css_manager = CssManager()
        self.keys = KeyManager(self.app.get_mode)
        self.layouts = LayoutManager(self.app)
        self.formatter = Formatter(self.app)

        self.css_manager.refresh_css()

    def no_op(self):
        pass

    def notify(self, message: str) -> None:
        self.app.notify(message)

    async def handle_key(self, key: str) -> None:
        func = self.keys.register_key(key)
        if func is not None:
            func()
        else:
            await self.focused.handle_keypress(key)

    def trigger_event(self, event: DooitEvent):
        event_name = event.snake_case
        for obj in self.plugin_manager.events[event_name]:
            obj(self)

    # -----------------------------------------

    @property
    def focused(self) -> ModelTree:
        focused = self.app.focused
        if isinstance(focused, ModelTree):
            return focused

        raise ValueError(f"Expected BaseTree, got {type(focused)}")

    def switch_focus(self):
        if self.app.bar_switcher.is_focused:
            return

        if w := self.app.focused:
            w.post_message(SwitchTab())

    def move_down(self):
        self.focused.action_cursor_down()

    def move_up(self):
        self.focused.action_cursor_up()

    def shift_up(self):
        self.focused.shift_up()

    def shift_down(self):
        self.focused.shift_down()

    def go_to_top(self):
        self.focused.action_first()

    def go_to_bottom(self):
        self.focused.action_last()

    def edit(self, property: str):
        self.focused.start_edit(property)

    def edit_description(self):
        return self.edit("description")

    def edit_due(self):
        return self.edit("due")

    def edit_recurrence(self):
        return self.edit("recurrence")

    def add_sibling(self):
        self.focused.add_sibling()

    def toggle_expand(self):
        self.focused.toggle_expand()

    def toggle_expand_parent(self):
        self.focused.toggle_expand_parent()

    def add_child_node(self):
        self.focused.add_child_node()

    def remove_node(self):
        self.focused.remove_node()

    def start_search(self):
        self.focused.start_search()

    def start_sort(self):
        self.focused.start_sort()

    def set_bar(self, widgets: List[StatusBarWidget]):
        self.app.bar.set_widgets(widgets)
