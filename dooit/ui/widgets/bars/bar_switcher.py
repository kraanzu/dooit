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
            self.status_bar,
            id="status_bar",
            set_current=True,
        )
