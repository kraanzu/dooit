from textual_extras.widgets import TextInput
from rich.text import TextType
from textual_extras.events import TextChanged


class Entry(TextInput):
    def __init__(self, name: str | None = None) -> None:
        super().__init__(name)

    def _format_text(self, text: str) -> str:
        return text

    def render_panel(self, text: TextType):
        return text

    async def handle_keypress(self, key: str) -> None:
        await super().handle_keypress(key)
        await self.emit(TextChanged(self))
        self.refresh()
