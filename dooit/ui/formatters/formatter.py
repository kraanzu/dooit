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

    def cursor_highlight(self, text: str, is_highlighted: bool, editing: str):
        if is_highlighted:
            return (
                self.colored(text, "b " + self.STYLE_EDITING)
                if editing != "none"
                else self.colored(text, "b " + self.STYLE_HIGHLIGHT)
            )

        return self.colored(text, "d " + self.STYLE_DIM)

    def color_combo(self, icon: str, text: str, color: str):
        return self.colored(f"[b] {icon}[/b]{text}", color)

    def colored(self, text: str, color: str):
        return f"[{color}]{text}[/{color}]"

    def style(
        self,
        column: str,  # column name
        item: model_type,  # workspace obj
        is_highlighted: bool,
        editing: str,
        kwargs: Dict[str, str],  # display items,
    ) -> Text:
        func_name = f"style_{column}"
        func = getattr(self, func_name)
        res = func(item, is_highlighted, editing, kwargs)
        return Text.from_markup(res)
