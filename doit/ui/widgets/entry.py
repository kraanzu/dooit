from typing import Literal
from textual import events
from textual_extras.widgets import TextInput
from rich.text import TextType
from textual_extras.events import TextChanged
from textual_extras.widgets.single_level_tree_edit import SimpleInput


class Entry(TextInput):
    """
    A Simple subclass of TextInput widget with no borders
    """

    def __init__(self, name: str | None = None) -> None:
        super().__init__(name, placeholder="")
        self.name = name
        self.about = SimpleInput()
        self.urgency = 1
        self.tags = []
        self.status = "PENDING"
        self.due = SimpleInput()
        self.focused = None

    def make_focus(self, part: Literal["about", "due"]):
        eval(f"self.{part}.on_focus()")
        self.focused = part

    def remove_focus(self):
        if self.focused:
            eval(f"self.{self.focused}.on_blur()")

    async def send_key(self, event: events.Key):
        if self.focused:
            await eval(f"self.{self.focused}.on_key(event)")

    def mark_complete(self) -> None:
        self.status = "COMPLETE"

    def mark_pending(self) -> None:
        self.status = "PENDING"

    def mark_overdue(self) -> None:
        self.status = "OVERDUE"

    def increase_urgency(self) -> None:
        self.urgency += 1

    def decrease_urgency(self) -> None:
        self.urgency = max(self.urgency - 1, 0)

    def _format_text(self, text: str) -> str:
        return text

    def render_panel(self, text: TextType) -> TextType:
        return text

    async def handle_keypress(self, key: str) -> None:
        await super().handle_keypress(key)
        await self.emit(TextChanged(self))
        self.refresh()
