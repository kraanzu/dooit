from rich.console import RenderableType
from dooit.ui.events import ModeChanged
from textual import events
from typing import TYPE_CHECKING, Callable
from .._base import BarBase
from ...inputs._input import Input


if TYPE_CHECKING:
    from ..bar_switcher import BarSwitcher


class SearchBar(BarBase):
    def __init__(self, callback: Callable, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._search = Input(value="/")
        self._search.is_editing = True
        self.callback = callback

    @property
    def switcher(self) -> "BarSwitcher":
        from ..bar_switcher import BarSwitcher

        parent = self.parent
        if not isinstance(parent, BarSwitcher):
            raise ValueError("Parent is not BarSwitcher")

        return parent

    def dismiss(self, cancel: bool = False):
        if cancel:
            self.callback("")

        self._search.is_editing = False
        self.switcher.current = "status_bar"

    async def handle_key(self, event: events.Key) -> bool:
        if event.key == "enter":
            self.app.post_message(ModeChanged("NORMAL"))
            self.dismiss()

        elif event.key == "escape":
            self.dismiss(cancel=True)

        else:
            self._search.keypress(event.key)
            filter = self._search.value[1:]
            self.callback(filter)

        self.refresh()
        return True

    def render(self) -> RenderableType:
        return self._search.draw()
