from textual.widgets import ContentSwitcher


class BarSwitcher(ContentSwitcher):
    DEFAULT_CSS = """
    BarSwitcher {
        height: 1;
        width: 100%;
    }
    """

    async def on_mount(self):
        pass

