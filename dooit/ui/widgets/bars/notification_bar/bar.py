from typing import Literal
from rich.console import RenderableType
from .._base import BarBase

NotificationType = Literal["info", "warning", "error"]


class NotificationBar(BarBase):
    DEFAULT_CSS = """
    NotificationBar {
        padding-left: 1;
        padding-right: 1;
    }
    """

    def __init__(
        self,
        message: str,
        level: NotificationType = "info",
        auto_exit: bool = True,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.message = message
        self.level = level
        self.auto_exit = auto_exit
        self.focused = not auto_exit
        self.add_class(self.level)

    def on_mount(self):
        if self.auto_exit:
            self.set_interval(1, self.close)

    async def handle_keypress(self, key: str) -> None:
        self.dismiss(cancel=True)

    def render(self) -> RenderableType:
        return self.message
