from typing import Optional
from rich.text import TextType
from textual.app import ComposeResult
from textual.widget import Widget
from dooit.api.manager import manager
from dooit.ui.events import StatusType
from dooit.utils.conf_reader import config_man

from .status_widget import StatusWidget
from .utils import AutoHorizontal, StatusMiddle
from .status_message import StatusMessage

bar = config_man.get("bar")


class StatusBar(Widget):
    """
    A status bar widget for showing messages and looks :)
    """

    DEFAULT_CSS = """
        StatusBar {
            max-height: 1;
            min-width: 100%;
            column-span: 2;
            layout: horizontal;
        }
    """

    def __init__(self) -> None:
        super().__init__()
        self.status = "NORMAL"

    def set_message(self, message: TextType = "") -> None:
        self.query_one(StatusMessage).set_message(message)

    def clear_message(self) -> None:
        self.query_one(StatusMessage).clear()

    def set_status(self, status: StatusType) -> None:
        self.status = status
        self.refresh()

    def get_params(self):
        return {
            "status": self.status,
            "manager": manager,
        }

    async def replace_middle(self, new_widget: Optional[StatusMiddle] = None):
        with self.app.batch_update():
            widget = self.query_one(StatusMiddle)
            self.mount(new_widget or StatusMessage(), before=widget)
            widget.remove()

    async def start_search(self, id_: str):
        from .searcher import Searcher

        searcher = Searcher(id_)
        await self.replace_middle(searcher)
        searcher.start_edit()

    async def stop_search(self):
        await self.replace_middle(StatusMessage())

    def compose(self) -> ComposeResult:
        yield AutoHorizontal(*[StatusWidget(i) for i in bar["A"]], classes="dock-left")
        yield StatusMessage()
        yield AutoHorizontal(*[StatusWidget(i) for i in bar["C"]], classes="dock-right")
