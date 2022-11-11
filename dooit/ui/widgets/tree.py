import re
from functools import partial
from typing import Dict, Iterable, List, Optional, Union
from rich.align import Align
from rich.console import Group, RenderableType
from rich.panel import Panel
from rich.text import Text
from textual import events
from textual.reactive import Reactive
from textual.widget import Widget
from rich.table import Table, box

from .simple_input import SimpleInput
from ...api import Manager, manager, Model, Workspace, Todo
from ...ui.widgets.sort_options import SortOptions
from ...ui.events.events import ChangeStatus, Notify


class Component:
    """
    Component class to maintain each row's data
    """

    def __init__(
        self,
        item: Union[Todo, Workspace],
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

    def refresh_item(self, field: str) -> None:
        self.fields[field] = SimpleInput(
            value=getattr(
                self.item,
                field,
            )
        )

    def get_field_values(self) -> Iterable[SimpleInput]:
        return self.fields.values()

    def toggle_expand(self) -> None:
        self.expanded = not self.expanded

    def expand(self, expand: bool = True) -> None:
        self.expanded = expand


class VerticalView:
    """
    Vertical view to manage scrolling
    """

    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b

    def fix_view(self, current: int) -> None:
        if self.a < 0:
            self.shift(-self.a)

        if current <= self.a:
            self.shift(current - self.a)

        if self.b <= current:
            self.shift(current - self.b)

    def shift_upper(self, delta) -> None:
        self.a += delta

    def shift_lower(self, delta) -> None:
        self.b += delta

    def shift(self, delta: int) -> None:
        self.shift_lower(delta)
        self.shift_upper(delta)

    def height(self) -> int:
        return self.b - self.a

    def range(self) -> Iterable[int]:
        return range(self.a, self.b + 1)


class TreeList(Widget):
    """
    An editable tree widget
    """

    _has_focus = False
    current = Reactive(-1)
    _rows = {}

    def __init__(
        self,
        name: str | None = None,
        model: Manager = manager,
    ) -> None:
        super().__init__(name=name)
        self.model = model
        self.editing = "none"
        self.sort_menu = SortOptions()
        self.sort_menu.visible = False
        self.filter = SimpleInput()

    @property
    def EMPTY(self) -> List[RenderableType]:
        return [""]

    async def on_mount(self) -> None:
        self._set_screen()
        self._refresh_rows()

    def commit(self) -> None:
        manager.commit()

    # ------------ INTERNALS ----------------

    def toggle_highlight(self) -> None:
        self._has_focus = not self._has_focus
        self.refresh()

    @property
    def has_focus(self) -> bool:
        return self._has_focus

    @property
    def component(self) -> Optional[Component]:
        if self.current != -1:
            return self.row_vals[self.current]

    @property
    def item(self) -> Optional[Workspace | Todo]:
        if self.component:
            return self.component.item

    # --------------------------------------

    def _fix_view(self) -> None:
        return self.view.fix_view(self.current)

    def _set_screen(self) -> None:
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

    def _setup_table(self) -> None:
        self.table = Table.grid(expand=True)

    def _get_children(self, model: Model) -> List[Workspace]:
        return model.workspaces

    def _refresh_rows(self) -> None:
        _rows_copy = self._rows
        self._rows = {}

        def add_rows(item: Workspace, nest_level=0):

            name = item.name
            path = item.path

            def push_item(item: Workspace):
                self._rows[name] = _rows_copy.get(
                    name,
                    Component(
                        item, nest_level, len(self._rows)
                    ),  # defaults to a new Component
                )
                self._rows[name].index = len(self._rows) - 1

            if pattern := self.filter.value:
                if re.findall(pattern, item._desc):
                    push_item(item)
                for i in self._get_children(item):
                    add_rows(i, nest_level + 1)
            else:
                push_item(item)
                if self._rows[name].expanded:
                    for i in self._get_children(item):
                        add_rows(i, nest_level + 1)

        for i in self._get_children(self.model):
            add_rows(i)

        self.row_vals: List[Component] = list(self._rows.values())
        self.refresh()

    async def _start_edit(self, field: str) -> None:
        if field == "none":
            return

        if not self.component:
            return

        if field == "desc":
            await self.emit(ChangeStatus(self, "INSERT"))
        elif field == "tags":
            await self.emit(ChangeStatus(self, "TAG"))
        else:
            await self.emit(ChangeStatus(self, "DATE"))

        self.component.fields[field].on_focus()
        self.editing = field

    async def _cancel_edit(self):
        await self._stop_edit(edit=False)

    async def _stop_edit(self, edit: bool = True) -> None:
        if self.editing == "none":
            return

        if not self.component:
            return

        simple_input = self.component.fields[self.editing]

        if not edit:
            val = getattr(
                self.component.item,
                self.editing,
            )
            simple_input.value = val

        res = self.component.item.edit(
            self.editing,
            simple_input.value,
        )

        simple_input.on_blur()
        self.component.refresh_item(self.editing)
        self.editing = "none"

        await self.emit(Notify(self, res.text()))
        await self.emit(ChangeStatus(self, "NORMAL"))

        if not res.ok:
            await self.remove_item()
        else:
            self.commit()

    async def _start_filtering(self) -> None:
        self.filter.on_focus()
        await self.emit(Notify(self, self.filter.render()))

    async def _stop_filtering(self) -> None:
        self.filter.clear()
        self._refresh_rows()
        await self.emit(Notify(self, self.filter.render()))
        await self.emit(ChangeStatus(self, "NORMAL"))

    def _add_child(self) -> Model:
        ...

    def _drop(self, _item=None) -> None:
        ...

    def _add_sibling(self) -> Model:
        ...

    def _next_sibling(self) -> Optional[Model]:
        ...

    def _prev_sibling(self) -> Optional[Model]:
        ...

    def _shift_up(self) -> None:
        ...

    def _shift_down(self) -> None:
        ...

    async def remove_item(self) -> None:
        if not self.item:
            return

        item = self.item
        self.current = min(self.current, len(self.row_vals) - 2)
        self._drop(item)
        self._refresh_rows()

        self.commit()
        self.refresh()

    async def add_child(self) -> None:

        if self.component and self.item:
            self.component.expand()

        self._add_child()
        self._refresh_rows()
        await self.move_down()
        await self._start_edit("desc")

    async def add_sibling(self) -> None:

        if not self.item:
            child = self._add_child()
            self._refresh_rows()
            self.current = self._rows[child.name].index
            await self._start_edit("desc")
            return

        self._add_sibling()
        self._refresh_rows()
        await self.to_next_sibling("desc")

    async def to_next_sibling(self, edit: Optional[str] = None) -> None:
        if not self.item:
            return

        await self._move_to_item(self._next_sibling(), edit)

    async def to_prev_sibling(self, edit: Optional[str] = None) -> None:
        if not self.item:
            return

        await self._move_to_item(self._prev_sibling(), edit)

    async def _move_to_item(
        self, item: Optional[Model], edit: Optional[str] = None
    ) -> None:
        if item is None:
            return

        self.current = self._rows[item.name].index
        if edit:
            await self._start_edit(edit)

    async def shift_up(self) -> None:
        if not self.item:
            return

        self._shift_up()
        self._refresh_rows()
        await self.move_up()
        self.commit()

    async def shift_down(self) -> None:
        if not self.item:
            return

        self._shift_down()
        self._refresh_rows()
        await self.move_down()
        self.commit()

    async def move_up(self) -> None:
        if self.current:
            self.current -= 1

    async def move_down(self) -> None:
        self.current = min(self.current + 1, len(self.row_vals) - 1)

    async def move_to_top(self) -> None:
        self.current = 0

    async def move_to_bottom(self) -> None:
        self.current = len(self.row_vals) - 1

    async def toggle_expand(self) -> None:
        if not self.component:
            return

        self.component.toggle_expand()
        self._refresh_rows()

    async def toggle_expand_parent(self) -> None:
        if not self.item:
            return

        parent = self.item.parent
        if parent and not isinstance(parent, Manager):
            index = self._rows[parent.name].index
            self.current = index

        await self.toggle_expand()

    def sort(self, attr: str) -> None:
        if self.item:
            curr = self.item.name
            self.item.sort(attr)
            self._refresh_rows()
            self.current = self._rows[curr].index
            self.commit()

    async def show_sort_menu(self) -> None:
        self.sort_menu.visible = True

    async def check_extra_keys(self, _event: events.Key) -> None:
        pass

    async def handle_tab(self) -> None:
        pass

    async def handle_key(self, event: events.Key) -> None:

        key = event.key

        if self.editing != "none":
            field = self.row_vals[self.current].fields[self.editing]

            if key == "escape":
                await self._cancel_edit()
            elif key == "enter":
                await self._stop_edit()
            else:
                await field.handle_keypress(event.key)

        else:

            if self.sort_menu.visible:
                await self.sort_menu.handle_key(event)

            elif self.filter.has_focus:
                await self.filter.handle_keypress(event.key)
                await self.emit(Notify(self, self.filter.render()))
                self._refresh_rows()
                self.current = 0

            else:

                keybinds = {
                    "escape": self._stop_filtering,
                    "tab": self.handle_tab,
                    "k": self.move_up,
                    "up": self.move_up,
                    "K": self.shift_up,
                    "shift+up": self.shift_up,
                    "j": self.move_down,
                    "down": self.move_down,
                    "J": self.shift_down,
                    "shift+down": self.shift_down,
                    "i": partial(self._start_edit, "desc"),
                    "z": self.toggle_expand,
                    "Z": self.toggle_expand_parent,
                    "A": self.add_child,
                    "a": self.add_sibling,
                    "x": self.remove_item,
                    "g": self.move_to_top,
                    "home": self.move_to_top,
                    "G": self.move_to_bottom,
                    "s": self.show_sort_menu,
                    "/": self._start_filtering,
                }

                if key in keybinds:
                    await keybinds[key]()

        await self.check_extra_keys(event)
        self.refresh(layout=True)

    def add_row(self, _item: Component, _highlight: bool) -> None:  # noqa
        ...

    def _stylize(
        self,
        fmt: Dict[str, str],
        highlight: bool,
        kwargs: Dict[str, str],
    ) -> Text:
        if highlight:
            if self.editing == "none":
                text: str = fmt["highlight"]
            else:
                text: str = fmt["edit"]
        else:
            text: str = fmt["dim"]

        text = text.format(**kwargs)
        return Text.from_markup(text)

    def make_table(self) -> None:
        self._setup_table()

        # for i in self.view.range():
        for i in range(len(self.row_vals)):
            try:
                self.add_row(self.row_vals[i], i == self.current)
            except:
                pass

    def push_row(self, row: List[Text], padding: int) -> None:
        if pattern := self.filter.value:
            for i in row:
                i.highlight_regex(pattern, style="b red")

        else:
            pad = " " * padding
            row = [Text(pad) + i for i in row]

        if row:
            self.table.add_row(*row)

    def render(self) -> RenderableType:

        if self.sort_menu.visible:
            to_render = self.sort_menu.render()
        elif not self.row_vals:
            to_render = Align.center(
                Group(
                    *[Align.center(i) for i in self.EMPTY],
                ),
                vertical="middle",
            )
        else:
            self.make_table()
            to_render = self.table

        height = self._size.height
        return Panel(
            to_render,
            expand=True,
            height=height,
            box=box.HEAVY,
            border_style="cyan" if self._has_focus else "dim white",
        )

    # async def on_resize(self, event: events.Resize) -> None:
    #     self._set_view()
    #     return await super().on_resize(event)
