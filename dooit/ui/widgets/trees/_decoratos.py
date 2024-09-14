from typing import Callable, TYPE_CHECKING
from textual.widgets.option_list import OptionDoesNotExist

if TYPE_CHECKING:
    from .model_tree import ModelTree
    ModelTreeFunc = Callable[[ModelTree], None]


def fix_highlight(func: "ModelTreeFunc") -> "ModelTreeFunc":

    def wrapper(self: "ModelTree") -> None:
        highlighted_id = self.node.id
        highlighted_index = self.highlighted

        assert highlighted_id is not None
        func(self)

        try:
            if self.get_option(highlighted_id):
                self.highlighted = self.get_option_index(highlighted_id)
        except OptionDoesNotExist:
            self.highlighted = min(highlighted_index or -1, len(self._options) - 1)

    return wrapper
