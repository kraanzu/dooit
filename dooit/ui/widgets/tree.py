from os import get_terminal_size
from typing import List, Tuple
from rich.console import RenderableType
from rich.panel import Panel
from rich.style import StyleType
from textual import events
from textual.widget import Widget
from rich.table import Table, box
from rich.text import Text

from .simple_input import SimpleInput
from ...api import manager, Model


class Component:
    def __init__(self, item: Model, depth: int = 0, expanded: bool = False) -> None:
        self.item = item
        self.expanded = expanded
        self.depth = depth
        self.fields = {
            field: SimpleInput(
                value=getattr(item, field),
            )
            for field in item.fields
        }

    def get_field_values(self):
        return self.fields.values()

    def toggle_expand(self):
        self.expanded = not self.expanded


class TreeList(Widget):
    _current = 0
    _rows = {}

    def __init__(
        self,
        name: str | None = None,
        style_off: StyleType = "",
        style_on: StyleType = "",
        style_edit: StyleType = "",
        model: Model = manager,
    ) -> None:
        super().__init__(name)
        self.style_off = style_off
        self.style_on = style_on
        self.style_edit = style_edit
        self.model = model
        self.editing = "none"

    async def on_mount(self):
        self._set_screen()

    # ------------ INTERNALS ----------------

    @property
    def current(self) -> int:
        return self._current

    @current.setter
    def current(self, value) -> None:
        if value < 0 or value >= len(self.row_vals):
            return

        self._current = value
        self._fix_view()
        self.refresh()

    # --------------------------------------

    def _set_screen(self):
        y = get_terminal_size()[1]
        self._view = [0, y]

    def _set_view(self) -> None:
        prev_size = self._view[1] - self._view[0]
        curr_size = get_terminal_size()[1]
        diff = prev_size - curr_size

        if diff <= 0:
            self._view[0] += diff
        else:
            bottom = self._view[1] - diff
            bottom = max(self.current + 1, bottom)
            self._view[0] = bottom - curr_size
            self._view[1] = bottom

        self._fix_view()

    def _fix_view(self):
        if self._view[0] < 0:
            diff = abs(self._view[0])
            self._view[0] += diff
            self._view[1] += diff

        if self.current >= self._view[1]:
            diff = self.current - self._view[1] + 1
            self._view[0] += diff
            self._view[1] += diff

        if self.current < self._view[0]:
            diff = self._view[0] - self.current
            self._view[0] -= diff
            self._view[1] -= diff

    def _get_table(self) -> Table:
        return Table.grid(expand=True)

    def _refresh_rows(self):
        _rows_copy = self._rows
        self._rows = {}

        def add_rows(item: Model = self.model, nest_level=0):

            name = item.name
            self._rows[name] = _rows_copy.get(
                name,
                Component(item, nest_level),  # defaults to a new Component
            )

            if self._rows[name].expanded:
                for i in item.children:
                    add_rows(i, nest_level + 1)

        for i in self.model.children:
            add_rows(i)

        self.row_vals: List[Component] = list(self._rows.values())

    def _stylize_item(
        self,
        item,
        highlight: bool = False,
    ):
        return [
            Text(
                i,
                style=self.style_on if highlight else self.style_off,
            )
            for i in item
        ]

    def _start_edit(self, field: str):
        self.row_vals[self.current].fields[field].on_focus()
        self.editing = field

    def remove_item(self):
        pass

    def add_sibling(self):
        pass

    def add_child(self):
        pass

    def move_up(self):
        self.current -= 1

    def move_down(self):
        self.current += 1

    def toggle_expand(self):
        self.row_vals[self.current].toggle_expand()

    async def handle_key(self, event: events.Key):

        key = event.key

        if self.editing != "none":
            field = self.row_vals[self.current].fields[self.editing]

            if key == "escape":
                self.editing = "none"
                field.on_blur()
            else:
                await field.handle_keypress(event.key)

        else:
            match key:
                case "k" | "up":
                    self.move_up()
                case "j" | "down":
                    self.move_down()
                case "i":
                    self._start_edit("about")
                case "d":
                    self._start_edit("date")
                case "z":
                    self.toggle_expand()

        self.refresh(layout=True)

    def _check_valid(self, depth: int) -> Tuple[int, bool]:
        return depth, True

    def add_row(self, row: Component, highlight: bool):
        depth, ok = self._check_valid(row.depth)
        if not ok:
            return

        padding = "  " * depth
        item = [padding + str(i.render()) for i in row.get_field_values()]
        self.table.add_row(*self._stylize_item(item, highlight))

    def render(self) -> RenderableType:
        self._refresh_rows()

        self.table = self._get_table()
        for i in range(self._view[0], self._view[1] + 1):
            try:
                self.add_row(self.row_vals[i], i == self.current)
            except:
                pass

        height = self._size.height
        return Panel(
            self.table,
            expand=True,
            height=height,
            box=box.HEAVY,
        )

    async def on_resize(self, event: events.Resize) -> None:
        self._set_view()
        return await super().on_resize(event)
