from textual.widgets import ContentSwitcher


class FlexibleSwitcher(ContentSwitcher):
    """
    Also allows to add more widgets to the switcher
    """

    DEFAULT_CSS = """
    FlexibleSwitcher {
        height: 1fr;
        width: 1fr;
    }
    """

    async def add_widget(self, widget):
        await self.mount(widget)
