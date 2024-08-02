import pyperclip
from typing import Optional
from dooit.ui.widgets.renderers.base_renderer import ModelType


class Input:
    """
    A simple single line Text Input
    """

    _cursor_position: int = 0
    _cursor: str = "|"
    highlight_pattern = ""
    value = ""
    is_editing = False

    def draw(self) -> str:
        if self.is_editing:
            text = self._render_text_with_cursor()
        else:
            text = self.value

        return text

    def render(self) -> str:
        return self.draw().strip()

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
        self.is_editing = True

    def stop_edit(self) -> None:
        self.is_editing = False

    def clear(self) -> None:
        """
        Clears the Input Box
        """
        self.value = ""
        self._cursor_position = 0

    def _insert_text(self, text: Optional[str] = None) -> None:
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

    def _move_cursor_backward(self, word=False, delete=False) -> None:
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

    def _move_cursor_forward(self, word=False, delete=False) -> None:
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

    def clear_input(self) -> None:
        self.move_cursor_to_end()
        while self.value:
            self.keypress("backspace")

    def move_cursor_to_end(self) -> None:
        self._cursor_position = len(self.value)

    def keypress(self, key: str) -> None:
        # Moving backward
        if key == "left":
            self._move_cursor_backward()

        elif key == "ctrl+left":
            self._move_cursor_backward(word=True)

        elif key == "backspace":  # Backspace
            self._move_cursor_backward(delete=True)

        elif key == "ctrl+w":
            self._move_cursor_backward(word=True, delete=True)

        # Moving forward
        elif key == "right":
            self._move_cursor_forward()

        elif key == "ctrl+right":
            self._move_cursor_forward(word=True)

        elif key == "delete":
            self._move_cursor_forward(delete=True)

        elif key == "ctrl+delete":
            self._move_cursor_forward(word=True, delete=True)

        elif key == "ctrl+l":
            self.clear_input()

        # EXTRAS
        elif key == "home":
            self._cursor_position = 0

        elif key == "end":
            self.move_cursor_to_end()

        elif key == "tab":
            self._insert_text("\t")

        elif key.startswith("events.Paste:"):
            self._insert_text(key[13:])

        elif len(key) == 1:
            self._insert_text(key)


class SimpleInput(Input):
    """
    A simple single line Text Input widget
    """

    _cursor_position: int = 0
    _cursor: str = "|"

    def __init__(self, model: ModelType) -> None:
        self.model = model
        self.value = getattr(model, self._property)
        self._cursor_position = len(self.value)
        super().__init__()

    @property
    def _property(self) -> str:
        return self.__class__.__name__.lower()

    # TODO: move to validation
    #
    # @property
    # def empty_result(self) -> Result:
    #     return Warn(f"{self.__class__.__name__} cannot be empty!")

    def refresh_value(self) -> str:
        self.value = getattr(self.model, self._property)
        return self.value

    def stop_edit(self, cancel: bool = False) -> None:
        super().stop_edit()

        if not cancel:
            res = self.model.edit(self._property, self.value)
        else:
            value = self.refresh_value()
            # if value:
            #     res = Ok()
            # else:
            #     res = Ok() if self.refresh_value() else self.empty_result

        self.refresh_value()

    def cancel_edit(self) -> None:
        return self.stop_edit(cancel=True)

    def keypress(self, key: str) -> None:
        super().keypress(key)

        if key == "escape":
            if True:
                self.stop_edit()
            else:
                self.cancel_edit()
