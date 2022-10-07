from typing import List, Optional, Tuple
from rich.console import RenderableType
from rich.panel import Panel
from rich.style import StyleType
from textual import events
from textual.widget import Widget
from rich.table import Table, box
from rich.text import Text

from .simple_input import SimpleInput
from ...api.manager import manager, Model
from ...api.model import MaybeModel


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

    def expand(self, expand: bool = True):
        self.expanded = expand


class VerticalView:
    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b

    def fix_view(self, current: int):
        if self.a < 0:
            self.shift(-self.a)

        if current <= self.a:
            self.shift(current - self.a)

        if self.b <= current:
            self.shift(current - self.b)

    def shift_upper(self, delta):
        self.a += delta

    def shift_lower(self, delta):
        self.b += delta

    def shift(self, delta: int):
        self.shift_lower(delta)
        self.shift_upper(delta)

    def height(self):
        return self.b - self.a


class TreeList(Widget):
    _has_focus = False
    _current = -1
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

    def toggle_highlight(self):
        self._has_focus = not self._has_focus
        self.refresh()

    @property
    def has_focus(self):
        return self._has_focus

    @property
    def current(self) -> int:
        return self._current

    @current.setter
    def current(self, value) -> None:

        if not self.row_vals:
            self._current = -1
            return

        value = min(max(0, value), len(self.row_vals) - 1)
        self._current = value
        self._fix_view()
        self.refresh()

    @property
    def component(self):
        if self.row_vals:
            return self.row_vals[self.current]
        else:
            return Component(self.model)

    @property
    def item(self):
        return self.component.item

    # --------------------------------------

    def _fix_view(self):
        self.view.fix_view(self.current)

    def _set_screen(self):
        y = self._size.height - 3  # Panel
        self.view = VerticalView(0, y)

    def _set_view(self) -> None:
        prev_size = self.view.height()
        curr_size = self._size.height - 3  # Panel
        diff = prev_size - curr_size

        if diff <= 0:
            self.view.shift_upper(diff)
        else:
            self.view.shift_lower(-diff)
            bottom = max(self.current + 1, self.view.b)
            self.view.a = bottom - curr_size
            self.view.b = bottom

        self._fix_view()

    def _get_table(self) -> Table:
        return Table.grid(expand=True)

    def _get_children(self, model: Model):
        return model.children

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
            self._rows[name].index = len(self._rows) - 1

            if self._rows[name].expanded:
                for i in self._get_children(item):
                    add_rows(i, nest_level + 1)

        for i in self._get_children(self.model):
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

    async def _start_edit(self, field: str):
        if self.component:
            self.component.fields[field].on_focus()
            self.editing = field

    async def _stop_edit(self):
        self.component.fields[self.editing].on_blur()
        self.component.item.edit(
            self.editing,
            self.component.fields[self.editing].value,
        )
        self.editing = "none"

    async def remove_item(self):
        self.item.drop()
        self._refresh_rows()
        self.current = self._current

    async def add_child(self):

        if not self.item:
            return

        self.component.expand()
        self.item.add_child()
        self._refresh_rows()
        await self.move_down()
        await self._start_edit("about")

    async def add_sibling(self):

        if not self.row_vals:
            manager.add_child()
            self._refresh_rows()
            await self._start_edit("about")
            return

        self.item.add_sibling()
        self._refresh_rows()
        await self.to_next_sibling("about")

    async def to_next_sibling(self, edit: Optional[str] = None):
        await self._move_to_item(self.item.next_sibling(), edit)

    async def to_prev_sibling(self, edit: Optional[str] = None):
        await self._move_to_item(self.item.prev_sibling(), edit)

    async def _move_to_item(self, item: MaybeModel, edit: Optional[str]):
        if not item:
            return

        self.current = self._rows[item.name].index
        if edit:
            await self._start_edit(edit)

    async def shift_up(self):
        self.item.shift_up()
        self._refresh_rows()
        await self.move_up()

    async def shift_down(self):
        self.item.shift_down()
        self._refresh_rows()
        await self.move_down()

    async def move_up(self):
        self.current -= 1

    async def move_down(self):
        self.current += 1

    async def move_to_top(self):
        self.current = 0

    async def move_to_bottom(self):
        self.current = len(self.row_vals)

    async def toggle_expand(self):
        self.component.toggle_expand()
        self._refresh_rows()

    async def toggle_expand_parent(self):
        parent = self.item.parent
        if parent and parent.name != "Manager":
            index = self._rows[parent.name].index
            self.current = index

    def check_extra_keys(self):
        pass

    async def handle_tab(self):
        pass

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
                case "ctrl+i":
                    await self.handle_tab()
                case "k" | "up":
                    await self.move_up()
                case "K":
                    await self.shift_up()
                case "j" | "down":
                    await self.move_down()
                case "J":
                    await self.shift_down()
                case "i":
                    await self._start_edit("about")
                # case "d":
                #     await self._start_edit("due")
                case "z":
                    await self.toggle_expand()
                case "Z":
                    await self.toggle_expand_parent()
                case "A":
                    await self.add_child()
                case "a":
                    if self.row_vals:
                        await self.add_sibling()
                    else:
                        await self.add_child()
                case "x":
                    await self.remove_item()
                case "g":
                    await self.move_to_top()
                case "G":
                    await self.move_to_bottom()

        self.check_extra_keys()
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

    def make_table(self):
        self.table = self._get_table()
        # for i in range(self._view[0], self._view[1] + 1):
        for i in range(len(self.row_vals)):
            try:
                self.add_row(self.row_vals[i], i == self.current)
            except:
                pass

    def render(self) -> RenderableType:

        self.make_table()
        height = self._size.height
        return Panel(
            self.table,
            expand=True,
            height=height,
            box=box.HEAVY,
            border_style="cyan" if self._has_focus else "dim white",
        )

    async def on_resize(self, event: events.Resize) -> None:
        self._set_view()
        return await super().on_resize(event)
