from typing import Callable

from rich.console import RenderableType
from textual.widget import events
from .._base import BarBase


class ConfirmBar(BarBase):
    def __init__(self, callback: Callable, *args, **kwargs):
        super().__init__(callback, *args, **kwargs)

    def perform_action(self, cancel: bool):
        if not cancel:
            self.callback()

    async def handle_key(self, event: events.Key) -> bool:
        cancel = event.key.lower() != "y"
        self.dismiss(cancel)
        return True

    def render(self) -> RenderableType:
        return r"Are you sure? \[y/N]:"
