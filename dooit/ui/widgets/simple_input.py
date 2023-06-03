import pyperclip
from typing import Optional
from rich.text import Text
from textual.widget import Widget
from dooit.api.model import Result
from dooit.api.todo import Todo
from dooit.ui.events.events import ChangeStatus, CommitData
from dooit.utils.conf_reader import Config

config = Config()
RED = config.get("red")
YELLOW = config.get("yellow")
GREEN = config.get("green")


class Input(Widget):
    """
    A simple single line Text Input widget
    """

    _cursor_position: int = 0
    _cursor: str = "|"
    highlight_pattern = ""
    value = ""

    @property
    def is_editing(self) -> bool:
        return self.has_class("editing")

    def draw(self) -> str:
        if self.is_editing:
            text = self._render_text_with_cursor()
        else:
            text = self.value

        return text

    def apply_filter(self, pattern: str):
        self.highlight_pattern = pattern
        self.refresh()

    def render(self) -> Text:
        """
        Renders a Panel for the Text Input Box
        """
        value = Text.from_markup(self.draw().strip())
        if self.highlight_pattern:
            value.highlight_words(
                self.highlight_pattern.split(),
                "r #88c0d0",
                case_sensitive=False,
            )
        return value

    def _render_text_with_color(self, text: str, color: str) -> str:
        return f"[{color}]{text}[/{color}]"

    def _render_text_with_cursor(self) -> str:
        """
        Produces renderable Text object combining value and cursor
        """

        return (
            self.value[: self._cursor_position]
            + self._cursor
            + self.value[self._cursor_position :]
        )

    def start_edit(self) -> None:
        self.add_class("editing")
        self.refresh(layout=True)

    def stop_edit(self) -> Optional[Result]:
        self.remove_class("editing")

    def clear(self) -> None:
        """
        Clears the Input Box
        """
        self.value = ""
        self._cursor_position = 0
        self.refresh(layout=True)

    async def _insert_text(self, text: Optional[str] = None) -> None:
        """
        Inserts text where the cursor is
        """

        # Will throw an error if `xclip` if not installed on the linux(Xorg) system,
        # should work just fine on windows and mac

        if text is None:
            text = str(pyperclip.paste())

        self.value = (
            self.value[: self._cursor_position]
            + text
            + self.value[self._cursor_position :]
        )

        self._cursor_position += len(text)

    async def _move_cursor_backward(self, word=False, delete=False) -> None:
        """
        Moves the cursor backwards..
        Optionally jumps over a word when pressed ctrl+left
        Optionally deletes the letter in case of backspace
        """

        prev = self._cursor_position

        if not word:
            self._cursor_position = max(self._cursor_position - 1, 0)
        else:
            while self._cursor_position:
                if self.value[self._cursor_position - 1] != " " and (
                    self._cursor_position == 1
                    or self.value[self._cursor_position - 2] == " "
                ):
                    self._cursor_position -= 1
                    break

                self._cursor_position -= 1

        if delete:
            self.value = self.value[: self._cursor_position] + self.value[prev:]

    async def _move_cursor_forward(self, word=False, delete=False) -> None:
        """
        Moves the cursor forward..
        Optionally jumps over a word when pressed ctrl+right
        Optionally deletes the letter in case of del or ctrl+del
        """

        prev = self._cursor_position

        if not word:
            self._cursor_position = min(self._cursor_position + 1, len(self.value))
        else:
            while self._cursor_position < len(self.value):
                if (
                    self._cursor_position != prev
                    and self.value[self._cursor_position - 1] == " "
                    and (
                        self._cursor_position == len(self.value) - 1
                        or self.value[self._cursor_position] != " "
                    )
                ):
                    break

                self._cursor_position += 1

        if delete:
            self.value = self.value[:prev] + self.value[self._cursor_position :]
            self._cursor_position = prev  # Because the cursor never actually moved :)

    async def clear_input(self):
        self.move_cursor_to_end()
        while self.value:
            await self.keypress("backspace")

    def move_cursor_to_end(self):
        self._cursor_position = len(self.value)

    async def keypress(self, key: str) -> None:
        """
        Handles Keypresses
        """
        if key == "space":
            key = " "

        if key == "enter":
            self.stop_edit()

        # Moving backward
        elif key == "left":
            await self._move_cursor_backward()

        elif key == "ctrl+left":
            await self._move_cursor_backward(word=True)

        elif key == "backspace":  # Backspace
            await self._move_cursor_backward(delete=True)

        elif key == "ctrl+w":
            await self._move_cursor_backward(word=True, delete=True)

        # Moving forward
        elif key == "right":
            await self._move_cursor_forward()

        elif key == "ctrl+right":
            await self._move_cursor_forward(word=True)

        elif key == "delete":
            await self._move_cursor_forward(delete=True)

        elif key == "ctrl+delete":
            await self._move_cursor_forward(word=True, delete=True)

        elif key == "ctrl+l":
            await self.clear_input()

        # EXTRAS
        elif key == "home":
            self._cursor_position = 0

        elif key == "end":
            self.move_cursor_to_end()

        elif key == "tab":
            await self._insert_text("\t")

        # COPY-PASTA
        elif key == "ctrl+v":
            try:
                await self._insert_text()
            except Exception:
                return

        if len(key) == 1:
            await self._insert_text(key)

        self.refresh(layout=True)


class SimpleInput(Input):
    """
    A simple single line Text Input widget
    """

    _cursor_position: int = 0
    _cursor: str = "|"
    _status_colors = {
        "COMPLETED": GREEN,
        "PENDING": YELLOW,
        "OVERDUE": RED,
    }

    def __init__(self, model: Todo, classes: str = "") -> None:
        self._property: str = self.__class__.__name__.lower()
        id_ = f"{model.uuid}-{self._property}"
        self.model = model
        self.value = getattr(model, self._property)
        self._cursor_position = len(self.value)

        super().__init__(id=id_, classes="padding dim " + classes)
        self.styles.height = "auto"
        self.highlight_pattern = ""

    def refresh_value(self):
        self.value = getattr(self.model, self._property)
        self.refresh(layout=True)

    def stop_edit(self, cancel: bool = False) -> Optional[Result]:
        super().stop_edit()
        if not cancel:
            self.model.edit(self._property, self.value)

        self.post_message(ChangeStatus("NORMAL"))
        self.refresh_value()
        self.post_message(CommitData())
        self.refresh(layout=True)

    def cancel_edit(self):
        return self.stop_edit(cancel=True)

    async def keypress(self, key: str) -> None:
        await super().keypress(key)

        if key == "escape":
            self.cancel_edit()

    def _colorize_by_status(self, text: str) -> str:
        return self._render_text_with_color(
            text,
            self._status_colors[self.model.status],
        )
