from textual import events
from typing import Callable
from textual.widgets import ContentSwitcher
from .status_bar import StatusBar
from .search_bar import SearchBar
from .confirm_bar import ConfirmBar


class BarSwitcher(ContentSwitcher):
    DEFAULT_CSS = """
    BarSwitcher {
        height: 1;
        width: 100%;
    }
    """

    status_bar = StatusBar()

    @property
    def search_bar(self):
        return self.query_one(SearchBar)

    @property
    def is_focused(self):
        return self.current != "status_bar"

    async def on_mount(self):
        self.add_content(
            widget=self.status_bar,
            id="status_bar",
            set_current=True,
        )

    def switch_to_search(self, callback: Callable):
        search_bar = SearchBar(callback)
        self.add_content(
            widget=search_bar,
            id="search_bar",
            set_current=True,
        )

    def switch_to_confirm(self, callback: Callable):
        confirm_bar = ConfirmBar(callback)
        self.add_content(
            widget=confirm_bar,
            id="confirm_bar",
            set_current=True,
        )

    async def handle_key(self, event: events.Key) -> bool:
        if (bar := self.visible_content) and self.current != "status_bar":
            return await bar.handle_key(event)

        return True
