import re
import pyperclip
from typing import Optional
from rich.style import Style
from rich.text import Text
from textual.widget import Widget
from dooit.api.model import Ok, Result, Warn
from dooit.api.todo import Todo
from dooit.utils.conf_reader import config_man

WHITE = config_man.get("white")
RED = config_man.get("red")
YELLOW = config_man.get("yellow")
GREEN = config_man.get("green")
SEARCH_COLOR = config_man.get("SEARCH_COLOR")
SAVE_ON_ESCAPE = config_man.get("SAVE_ON_ESCAPE")
TAGS_COLOR = config_man.get("TODO").get("tags_color")


class Input(Widget):
    """
    A simple single line Text Input widget
    """

    DEFAULT_CSS = f"""
    Input {{
        color: {WHITE};
    }}
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

    def apply_filter(self, pattern: str) -> None:
        self.highlight_pattern = pattern
        self.refresh()

    def render(self) -> Text:
        """
        Renders a Panel for the Text Input Box
        """

        def make_links(text: Text):
            """
            Apply link opens to urls
            """

            pattern = r"https?://\S+|ftp://\S+"
            for i in re.findall(pattern, text.plain):
                style = Style.from_meta({"@click": f"app.open_url('{i}')"})
                text.highlight_words([i], style)

        def make_tags(text: Text):
            text.highlight_regex(r"\@\w+", TAGS_COLOR)

        value = Text.from_markup(self.draw().strip())
        make_links(value)
        make_tags(value)

        if self.highlight_pattern:
            value.highlight_words(
                self.highlight_pattern.split(),
                f"r {SEARCH_COLOR}",
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

    async def stop_edit(self) -> Optional[Result]:
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

    async def clear_input(self) -> None:
        self.move_cursor_to_end()
        while self.value:
            await self.keypress("backspace")

    def move_cursor_to_end(self) -> None:
        self._cursor_position = len(self.value)

    async def keypress(self, key: str) -> None:
        """
        Handles Keypresses
        """
        if key == "enter":
            await self.stop_edit()

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
        # elif key == "ctrl+v":
        #     try:
        #         await self._insert_text()
        #     except Exception:
        #         return
        elif key.startswith('events.Paste:'):
            await self._insert_text(key[13:])

        elif len(key) == 1:
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

    @property
    def empty_result(self) -> Result:
        return Warn(f"{self.__class__.__name__} cannot be empty!")

    def refresh_value(self) -> str:
        self.value = getattr(self.model, self._property)
        self.refresh(layout=True)
        return self.value

    async def stop_edit(self, cancel: bool = False) -> Optional[Result]:
        await super().stop_edit()
        from dooit.ui.widgets.tree import Tree

        if not cancel:
            res = self.model.edit(self._property, self.value)
        else:
            value = self.refresh_value()
            if value:
                res = Ok()
            else:
                res = Ok() if self.refresh_value() else self.empty_result

        self.refresh_value()
        await self.app.query_one(".focus", expect_type=Tree).stop_edit(res)
        return res

    async def cancel_edit(self) -> Optional[Result]:
        return await self.stop_edit(cancel=True)

    async def keypress(self, key: str) -> None:
        await super().keypress(key)

        if key == "escape":
            if SAVE_ON_ESCAPE:
                await self.stop_edit()
            else:
                await self.cancel_edit()

    def _colorize_by_status(self, text: str) -> str:
        return self._render_text_with_color(
            text,
            self._status_colors[self.model.status],
        )
