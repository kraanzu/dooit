from typing import Type, Dict
from rich.text import Text
from dooit.api import Model


class Formatter:
    model_type: Type[Model] = Model

    def __init__(
        self,
        format: Dict[str, str],
    ) -> None:
        self.format = format
        self.STYLE_DIM = format["dim"]
        self.STYLE_HIGHLIGHT = format["highlight"]
        self.STYLE_EDITING = format["editing"]

    def cursor_highlight(self, text: str, is_highlighted: bool, is_editing):
        if is_highlighted:
            return (
                self.colored(text, self.STYLE_EDITING)
                if is_editing
                else self.colored(text, self.STYLE_HIGHLIGHT)
            )

        return self.colored(text, self.STYLE_DIM)

    def colored(self, text: str, color: str):
        return f"[{color}]{text}[/{color}]"

    def style(
        self,
        column: str,  # column name
        item: model_type,  # workspace obj
        is_highlighted: bool,
        is_editing: bool,
        kwargs: Dict[str, str],  # display items,
    ) -> Text:
        func_name = f"style_{column}"
        func = getattr(self, func_name)
        res = func(item, is_highlighted, is_editing, kwargs)
        return Text.from_markup(res)
