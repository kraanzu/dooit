from textual.widgets import ContentSwitcher


class FlexibleSwitcher(ContentSwitcher):
    """
    Also allows to add more widgets to the switcher
    """

    DEFAULT_CSS = """
    FlexibleSwitcher {
        height: 100%;
        width: 100%;
    }
    """

    def add_widget(self, widget):
        self.mount(widget)
