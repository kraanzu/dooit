from typing import List

from rich.text import TextType
from textual.app import App

from dooit.ui.widgets.dashboard import Dashboard
from ._base import ApiComponent


class DashboardManager(ApiComponent):
    def __init__(self, app: App) -> None:
        super().__init__()
        self.app = app

    def set(self, items: List[TextType]):
        self.app.query_one(Dashboard).items = items
