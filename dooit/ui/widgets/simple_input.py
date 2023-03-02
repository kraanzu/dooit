import pyperclip
from typing import Any, Literal
from rich.style import StyleType
from rich.text import Text, TextType
from rich.box import Box
from rich.align import AlignMethod
from textual.widget import Widget
from textual import events
from textual.reactive import Reactive


class SimpleInput(Widget):
    """
    A simple single line Text Input widget
    """

    cursor: str = "|"
    _cursor_position: int = 0
    _has_focus: Reactive[bool] = Reactive(False)

    def __init__(
        self,
        name: str | None = None,
        value: Any = "",
        title: TextType = "",
        title_align: AlignMethod = "center",
        border_style: StyleType = "blue",
        box: Box | None = None,
        placeholder: Text = Text("", style="dim white"),
        password: bool = False,
        list: tuple[Literal["blacklist", "whitelist"], list[str]] = ("blacklist", []),
    ) -> None:
        super().__init__(name=name)
        self.title = title
        self.value = str(value)
        self.title_align: AlignMethod = title_align  # Silence compiler warning
        self.border_style: StyleType = border_style
        self.placeholder = placeholder
        self.password = password
        self.list = list
        self.box = box

        self._cursor_position = len(self.value)
        self.width = self.size.width - 4

    @property
    def has_focus(self) -> bool:
        return self._has_focus

    def render(self) -> Text:
        """
        Renders a Panel for the Text Input Box
        """

        if self.has_focus:
            text = self._render_text_with_cursor()
        else:
            if len(self.value) == 0:
                return self.placeholder
            else:
                text = self.value

        formatted_text = Text.from_markup(text)
        return formatted_text

    def _render_text_with_cursor(self) -> str:
        """
        Produces renderable Text object combining value and cursor
        """

        text = ""

        if self.password:
            text += "•" * self._cursor_position
            text += self.cursor
            text += "•" * (len(self.value) - self._cursor_position)
        else:
            text += self.value[: self._cursor_position]
            text += self.cursor
            text += self.value[self._cursor_position :]

        return text

    def on_focus(self, *_: events.Focus) -> None:
        self._has_focus = True

    def on_blur(self, *_: events.Blur) -> None:
        self._has_focus = False

    def clear(self) -> None:
        """
        Clears the Input Box
        """
        self.value = ""
        self._cursor_position = 0
        self.refresh()

    def _is_allowed(self, text: str) -> bool:
        if self.list[0] == "whitelist":
            for letter in text:
                if letter not in self.list[1]:
                    return False
        else:
            for letter in text:
                if letter in self.list[1]:
                    return False

        return True

    async def _insert_text(self, text: str | None = None) -> None:
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

    async def on_key(self, event: events.Key) -> None:
        """Send the key to the Input"""

        await self.handle_keypress(event.key)
        self.refresh()

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
            await self.handle_keypress("backspace")

    def move_cursor_to_end(self):
        self._cursor_position = len(self.value)

    async def handle_keypress(self, key: str) -> None:
        """
        Handles Keypresses
        """

        if key == "space":
            key = " "

        if key == "enter":
            self.on_blur()

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
            except:
                return

        if len(key) == 1:
            await self._insert_text(key)

        self.refresh()
