from rich.console import RenderableType
from textual import events
from typing import Callable
from .._base import BarBase
from ...inputs._input import Input


class SearchBar(BarBase):
    def __init__(self, callback: Callable, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._search = Input(value="/")
        self._search.is_editing = True
        self.callback = callback

    async def handle_key(self, event: events.Key) -> bool:
        self.notify(event.key)
        self._search.keypress(event.key)
        self.refresh()
        return True

    def render(self) -> RenderableType:
        return self._search.draw()
