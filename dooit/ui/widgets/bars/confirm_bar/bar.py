from typing import Callable
from rich.console import RenderableType
from .._base import BarBase

DEFFAULT_MSG = r"Are you sure? \[y/N]"


class ConfirmBar(BarBase):
    DEFAULT_CSS = """
    ConfirmBar {
        padding-left: 1;
        padding-right: 1;
    }
    """

    def __init__(
        self,
        callback: Callable,
        message: str = DEFFAULT_MSG,
        *args,
        **kwargs,
    ):
        super().__init__(callback, *args, **kwargs)
        self.message = message

    def perform_action(self, cancel: bool):
        if not cancel:
            self.callback()

    async def handle_keypress(self, key: str) -> None:
        cancel = key.lower() != "y"
        app = self.app

        self.dismiss(cancel)
        if cancel:
            app.notify_bar("The items were retained!", "info")
        else:
            app.notify_bar("The items were deleted!", "error")

    def render(self) -> RenderableType:
        return self.message
