from typing import TYPE_CHECKING, List
from dooit.ui.widgets.bars import StatusBarWidget
from ._base import ApiComponent

if TYPE_CHECKING:  # pragma: no cover
    from dooit.ui.tui import Dooit


class BarManager(ApiComponent):
    def __init__(self, app: "Dooit") -> None:
        super().__init__()
        self.app = app

    def set(self, widgets: List[StatusBarWidget]):
        self.app.bar.set_widgets(widgets)
