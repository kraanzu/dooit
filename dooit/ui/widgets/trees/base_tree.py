from typing import TYPE_CHECKING, Union
from textual.widgets import OptionList
from textual.widgets.option_list import Option
from dooit.api.todo import Todo
from dooit.api.workspace import Workspace
from collections import defaultdict
from dooit.ui.widgets.trees._decorators import require_highlighted_node

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
    @require_highlighted_node
    def node(self) -> Option:
        assert self.highlighted is not None
        return self.get_option_at_index(self.highlighted)

    # TODO: Uncomment this:
    #
    # def action_cursor_down(self) -> None:
    #     if self.highlighted == len(self._options) - 1:
    #         return
    #
    #     return super().action_cursor_down()
    #
    # def action_cursor_up(self) -> None:
    #     if self.highlighted == 0:
    #         return
    #
    #     return super().action_cursor_up()
