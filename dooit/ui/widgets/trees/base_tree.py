from typing import TYPE_CHECKING, Union
from textual.widgets import OptionList
from textual.widgets.option_list import Option
from dooit.api.todo import Todo
from dooit.api.workspace import Workspace
from collections import defaultdict

ModelType = Union[Todo, Workspace]

if TYPE_CHECKING:
    from ....ui.tui import Dooit


class BaseTree(OptionList, can_focus=True, inherit_bindings=False):
    expanded_nodes = defaultdict(bool)

    @property
    def tui(self) -> "Dooit":
        from ....ui.tui import Dooit

        if isinstance(self.app, Dooit):
            return self.app

        raise ValueError("App is not a Dooit instance")

    @property
    def node(self) -> Option:
        if self.highlighted is None:
            raise ValueError("No node is currently highlighted")

        return self.get_option_at_index(self.highlighted)

    def action_cursor_down(self) -> None:
        if self.highlighted == len(self._options) - 1:
            return

        return super().action_cursor_down()

    def action_cursor_up(self) -> None:
        if self.highlighted == 0:
            return

        return super().action_cursor_up()
