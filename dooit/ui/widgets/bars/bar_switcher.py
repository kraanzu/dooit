from typing import Callable
from textual.widgets import ContentSwitcher
from .status_bar import StatusBar
from .search_bar import SearchBar


class BarSwitcher(ContentSwitcher):
    DEFAULT_CSS = """
    BarSwitcher {
        height: 1;
        width: 100%;
    }
    """

    status_bar = StatusBar()

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
