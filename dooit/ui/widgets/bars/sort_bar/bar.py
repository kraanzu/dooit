from rich.console import RenderableType
from rich.text import Text
from dooit.ui.widgets.bars._base import BarBase
from dooit.api import DooitModel


class SortBar(BarBase):
    def __init__(self, model: DooitModel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model
        self.options = ["reverse"] + self.model.comparable_fields()
        self._selected = 0

    @property
    def selected(self) -> int:
        return self._selected

    @selected.setter
    def selected(self, val: int):
        val = max(val, 0)
        val = min(val, len(self.options) - 1)
        self._selected = val

        self.refresh()

    def perform_action(self, cancel: bool):
        if cancel:
            return

        selected = self.options[self.selected]
        if selected == "reverse":
            self.model.reverse_siblings()
        else:
            self.model.sort_siblings(selected)

    async def handle_keypress(self, key: str) -> None:
        if key == "escape":
            return self.dismiss(cancel=True)

        if key == "enter":
            return self.dismiss(cancel=False)

        if key == "left":
            self.selected -= 1
        elif key == "right":
            self.selected += 1

    def render(self) -> RenderableType:
        texts = [
            Text(f" {i} ", style="black on green" if index == self.selected else "")
            for index, i in enumerate(self.options)
        ]
        return Text.assemble(*texts)
