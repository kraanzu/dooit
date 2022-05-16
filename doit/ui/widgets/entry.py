from textual_extras.widgets import TextInput
from rich.text import TextType
from textual_extras.events import TextChanged
from ...src.utils.task import Task


class Entry(TextInput):
    """
    A Simple subclass of TextInput widget with no borders
    """

    def __init__(self, name: str | None = None) -> None:
        super().__init__(name, placeholder="hi")
        self.todo = Task()

    def mark_complete(self):
        self.todo.status = "COMPLETE"

    def mark_pending(self):
        self.todo.status = "PENDING"

    def mark_overdue(self):
        self.todo.status = "OVERDUE"

    def _format_text(self, text: str) -> str:
        return text

    def render_panel(self, text: TextType) -> TextType:
        return text

    async def handle_keypress(self, key: str) -> None:
        await super().handle_keypress(key)
        await self.emit(TextChanged(self))
        self.refresh()
