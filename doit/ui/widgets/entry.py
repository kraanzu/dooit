from textual_extras.widgets import TextInput
from rich.text import TextType
from textual_extras.events import TextChanged
from ...src.utils.task import Task


class Entry(TextInput):
    """
    A Simple subclass of TextInput widget with no borders
    """

    def __init__(self, name: str | None = None) -> None:
        super().__init__(name, placeholder="")
        self.todo = Task()

    def mark_complete(self) -> None:
        self.todo.status = "COMPLETE"

    def mark_pending(self) -> None:
        self.todo.status = "PENDING"

    def mark_overdue(self) -> None:
        self.todo.status = "OVERDUE"

    def increase_urgency(self) -> None:
        self.todo.urgency += 1

    def decrease_urgency(self) -> None:
        self.todo.urgency = max(self.todo.urgency - 1, 0)

    def _format_text(self, text: str) -> str:
        return text

    def render_panel(self, text: TextType) -> TextType:
        return text

    async def handle_keypress(self, key: str) -> None:
        await super().handle_keypress(key)
        await self.emit(TextChanged(self))
        self.refresh()
