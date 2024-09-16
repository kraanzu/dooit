from typing import Any, Callable, TYPE_CHECKING
from textual.widgets.option_list import OptionDoesNotExist

if TYPE_CHECKING:
    from .model_tree import ModelTree


def fix_highlight(func: Callable) -> Callable:

    def wrapper(self: "ModelTree", *args, **kwargs) -> Any:
        highlighted_id = self.node.id if self.highlighted else None
        highlighted_index = self.highlighted

        func(self, *args, **kwargs)

        try:
            if highlighted_id and self.get_option(highlighted_id):
                self.highlight_id(highlighted_id)
            else:
                self.highlighted = None

        except OptionDoesNotExist:
            self.highlighted = min(
                highlighted_index or -1,
                len(self._options) - 1,
            )

    return wrapper


def refresh_tree(func: Callable) -> Callable:

    def wrapper(self: "ModelTree", *args, **kwargs) -> Any:
        func(self, *args, **kwargs)
        self.force_refresh()

    return wrapper
