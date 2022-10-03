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
    def __init__(
        self,
        item: Model,
        depth: int = 0,
        index: int = 0,
        expanded: bool = False,
    ) -> None:
        self.item = item
        self.expanded = expanded
        self.depth = depth
        self.index = index
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
        style_off: StyleType = "dim grey50",
        style_on: StyleType = "bold white",
        style_edit: StyleType = "bold cyan",
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
        self._refresh_rows()

    # ------------ INTERNALS ----------------

    @property
    def current(self) -> int:
        return self._current

    @current.setter
    def current(self, value) -> None:
        value = min(max(0, value), len(self.row_vals) - 1)
        self._current = value
        self._fix_view()
        self.refresh()

    @property
    def component(self):
        return self.row_vals[self.current]

    @property
    def item(self):
        return self.component.item

    # --------------------------------------

    def _set_screen(self):
        y = get_terminal_size()[1] - 3  # Panel
        self._view = [0, y]

    def _set_view(self) -> None:
        prev_size = self._view[1] - self._view[0]
        curr_size = get_terminal_size()[1] - 3  # Panel
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
                Component(
                    item, nest_level, len(self._rows)
                ),  # defaults to a new Component
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

    async def _stop_edit(self):
        curr = self.row_vals[self.current]
        curr.fields[self.editing].on_blur()
        curr.item.edit(self.editing, curr.fields[self.editing].value)
        self.editing = "none"

    def remove_item(self):
        curr = self.row_vals[self.current]
        curr.item.drop()
        self._refresh_rows()
        # self.current = self._current

    def add_child(self):
        if not self.row_vals:
            return

        curr = self.row_vals[self.current]
        curr.toggle_expand()
        self.item.add_child()
        self._refresh_rows()
        self.move_down()
        self._start_edit("about")

    def add_sibling(self):

        if not self.row_vals:
            manager.add_child()
            self._refresh_rows()
            self._start_edit("about")
            return

        curr = self.row_vals[self.current].item
        curr.add_sibling()
        self._refresh_rows()

        self.move_down()
        self._start_edit("about")

    def shift_up(self):
        self.item.shift_up()
        self._refresh_rows()
        self.move_up()

    def shift_down(self):
        self.item.shift_down()
        self._refresh_rows()
        self.move_down()

    def move_up(self):
        self.current -= 1

    def move_down(self):
        self.current += 1

    def move_to_top(self):
        self.current = 0

    def move_to_bottom(self):
        self.current = len(self.row_vals)

    def toggle_expand(self):
        self.row_vals[self.current].toggle_expand()
        self._refresh_rows()

    def toggle_expand_parent(self):
        parent = self.item.parent
        if parent:
            index = self._rows[parent.name].index
            self.current = index

    async def handle_key(self, event: events.Key):

        key = event.key

        if self.editing != "none":
            field = self.row_vals[self.current].fields[self.editing]

            if key == "escape":
                await self._stop_edit()
            else:
                await field.handle_keypress(event.key)

        else:
            match key:
                case "k" | "up":
                    self.move_up()
                case "K":
                    self.shift_up()
                case "j" | "down":
                    self.move_down()
                case "J":
                    self.shift_down()
                case "i":
                    self._start_edit("about")
                case "d":
                    self._start_edit("date")
                case "z":
                    self.toggle_expand()
                case "Z":
                    self.toggle_expand_parent()
                case "A":
                    self.add_child()
                case "a":
                    self.add_sibling()
                case "x":
                    self.remove_item()
                case "g":
                    self.move_to_top()
                case "G":
                    self.move_to_bottom()

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
