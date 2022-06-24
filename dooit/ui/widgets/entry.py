from typing import Any, Literal
from textual import events
from rich.text import TextType
from string import printable as chars
from random import choice
from .simple_input import SimpleInput


def generate_uuid() -> str:
    """
    Generates a unique id for entries
    """
    uuid = ""
    for _ in range(32):
        uuid += choice(chars)
    return uuid


class Entry(SimpleInput):
    """
    A Simple subclass of TextInput widget with no borders
    """

    def __init__(self, name: str | None = None) -> None:
        super().__init__(name, placeholder="")
        self.name = name
        self.about = SimpleInput()
        self.urgency = 1
        self.status = "PENDING"
        self.due = SimpleInput()
        self.focused = None
        self.uuid = generate_uuid()

    async def make_focus(self, part: Literal["about", "due"]) -> None:
        eval(f"self.{part}.on_focus()")
        await eval(f"self.{part}.handle_keypress('end')")
        self.focused = part

    async def remove_focus(self) -> None:
        if self.focused:
            eval(f"self.{self.focused}.on_blur()")
            await eval(f"self.{self.focused}.handle_keypress('home')")

    async def send_key(self, event: events.Key) -> None:
        if self.focused:
            await eval(f"self.{self.focused}.on_key(event)")

    def increase_urgency(self) -> None:
        self.urgency = min(self.urgency + 1, 4)

    def decrease_urgency(self) -> None:
        self.urgency = max(self.urgency - 1, 1)

    def _format_text(self, text: str) -> str:
        return text

    def render_panel(self, text: TextType) -> TextType:
        return text

    async def handle_keypress(self, key: str) -> None:
        await super().handle_keypress(key)
        self.refresh()

    # DEPRECATED: will be removed in v0.3.0
    def encode(self) -> dict[str, Any]:
        return {
            "about": self.about.value,
            "urgency": self.urgency,
            "due": self.due.value,
            "status": self.status,
        }

    # DEPRECATED: will be removed in v0.3.0
    @classmethod
    def from_encoded(cls, data: dict[str, Any]) -> "Entry":
        entry = cls()
        entry.about.value = data["about"]
        entry.urgency = data["urgency"]
        entry.due.value = data["due"]
        entry.status = data["status"]
        return entry

    def to_txt(self) -> str:
        match self.status:
            case "PENDING":
                status = "x"
            case "COMPLETED":
                status = "X"
            case _:
                status = "O"  # OVERDUE

        return f"{status} ({self.urgency}) due:{self.due.value or 'None'} {self.about.value}"

    @classmethod
    def from_txt(cls, txt: str):
        status, urgency, due, *about = txt.split()

        match status:
            case "x":
                status = "PENDING"
            case "X":
                status = "COMPLETED"
            case _:
                status = "OVERDUE"

        about = " ".join(about)

        due = due[4:]
        if due == "None":
            due = ""

        urgency = int(urgency[1:-1])

        entry = cls()
        entry.about.value = about
        entry.urgency = urgency
        entry.due.value = due
        entry.status = status
        return entry
