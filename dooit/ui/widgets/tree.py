from os import get_terminal_size
from typing import List
from rich.style import StyleType
from textual import events
from textual.app import App
from textual.widget import Widget
from rich.table import Table
from rich.text import Text

from simple_input import SimpleInput
from model import manager, Model


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
        table = Table.grid(expand=True)
        table.add_column("a", ratio=7)
        table.add_column("b", ratio=2)
        table.add_column("c", ratio=1)

        return table

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
                overflow="ignore",
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

    def add_row(self, row: Component, highlight: bool):
        padding = "  " * row.depth
        item = [padding + str(i.render()) for i in row.get_field_values()]
        self.table.add_row(*self._stylize_item(item, highlight))

    def render(self):
        self._refresh_rows()

        self.table = self._get_table()

        for i in range(self._view[0], self._view[1] + 1):
            try:
                self.add_row(self.row_vals[i], i == self.current)
            except:
                pass

        return self.table

    async def on_resize(self, event: events.Resize) -> None:
        self._set_view()
        return await super().on_resize(event)


class A(App):
    async def on_mount(self):
        self.x = TreeList(
            style_off="dim white",
            style_on="bold white",
            style_edit="b cyan",
        )
        await self.view.dock(self.x)

    async def on_key(self, event: events.Key):
        await self.x.handle_key(event)
        self.refresh()


A.run()
