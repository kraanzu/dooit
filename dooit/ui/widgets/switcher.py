from textual.widgets import ContentSwitcher


class FlexibleSwitcher(ContentSwitcher):
    """
    Also allows to add more widgets to the switcher
    """

    def add_widget(self, widget):
        self.mount(widget)
