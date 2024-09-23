from .base import BaseScreen


class HelpScreen(BaseScreen):
    """
    Help Screen to view Help Menu
    """

    BINDINGS = [
        ("escape", "app.pop_screen", "Pop screen"),
    ]
