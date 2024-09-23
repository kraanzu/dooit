from typing import Callable
from rich.console import RenderableType
from textual.widget import events
from .._base import BarBase

DEFFAULT_MSG = r"Are you sure? \[y/N]"


class ConfirmBar(BarBase):
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

    def flash_confirm(self, cancelled: bool):
        if cancelled:
            self.message = "The items were deleted!"
        else:
            self.message = "The operation was cancelled!"

        self.refresh()
        self.set_interval(2, self.close)

    async def handle_key(self, event: events.Key) -> bool:
        cancel = event.key.lower() != "y"
        self.flash_confirm(cancel)
        self.dismiss(cancel, close = False)
        return True

    def render(self) -> RenderableType:
        return self.message
