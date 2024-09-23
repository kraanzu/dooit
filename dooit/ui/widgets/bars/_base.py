from typing import TYPE_CHECKING, Callable
from textual.widgets import Static

from ...events.events import ModeChanged

if TYPE_CHECKING:
    from .bar_switcher import BarSwitcher


class BarBase(Static):
    DEFAULT_CSS = """
    BarBase {
        height: 1;
        width: 100%;
    }
    """

    def __init__(self, callback: Callable = lambda: None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = callback

    @property
    def switcher(self) -> "BarSwitcher":
        from .bar_switcher import BarSwitcher

        parent = self.parent
        if not isinstance(parent, BarSwitcher):
            raise ValueError("Parent is not BarSwitcher")

        return parent

    def dismiss(self, cancel: bool = False):
        if cancel:
            self.callback("")

        self.app.post_message(ModeChanged("NORMAL"))

        _id = "status_bar"
        if self.id != _id:
            self.switcher.current = "status_bar"
            self.remove()
