import re
import pyperclip
from textual.geometry import Size
from typing import Any, Dict, Iterable, List, Literal, Optional, Type
from rich.align import Align
from rich.console import Group, RenderableType
from rich.panel import Panel
from rich.text import Text, TextType
from rich.table import Table, box
from textual import events
from textual.reactive import Reactive
from textual.widget import Widget
from dooit.ui.formatters import Formatter
from dooit.utils.keybinder import KeyBinder
from dooit.api import Manager, manager, Model
from dooit.ui.widgets.sort_options import SortOptions
from dooit.ui.events.events import ChangeStatus, Notify, SpawnHelp, StatusType
from dooit.utils.conf_reader import Config
from .simple_input import SimpleInput

PRINTABLE = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
conf = Config()
DIM = conf.get("BORDER_DIM")
LIT = conf.get("BORDER_LIT")


class Component:
    """
    Component class to maintain each row's data
    """

    def __init__(
        self,
        item,
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

    def refresh(self) -> None:
        for field in self.fields.keys():
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
            self.shift(abs(self.a))

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
        if self.a < 0:
            self.shift(abs(self.a))

        return range(self.a, self.b + 1)


class TreeList(Widget):
    """
    An editable tree widget
    """

    _has_focus = False
    _rows = {}
    current = Reactive(-1)
    options = []
    EMPTY: List
    model_type: Type[Model] = Model
    model_kind: Literal["workspace", "todo"]
    COLS: List
    styler: Formatter
    key_manager: KeyBinder

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
        self.sort_menu = SortOptions(
            name=f"Sort_{self.name}",
            options=self.options,
            parent_widget=self,
        )
        self.sort_menu.visible = False

    async def on_mount(self) -> None:
        self._set_screen()
        self._refresh_rows()

    def commit(self) -> None:
        manager.commit()

    async def _current_change_callback(self) -> None:
        pass

    # ------------ INTERNALS ----------------

    async def watch_current(self, value: int) -> None:
        if not self.row_vals:
            self.current = -1
        else:
            value = min(max(0, value), len(self.row_vals) - 1)
            self.current = value

        await self._current_change_callback()
        self._fix_view()
        self.refresh()

    async def notify(self, message: TextType):
        await self.emit(Notify(self, message))

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
    def item(self) -> Optional[Any]:
        if self.component:
            return self.component.item

    # --------------------------------------

    def _size_updated(
        self, size: Size, virtual_size: Size, container_size: Size
    ) -> None:
        super()._size_updated(size, virtual_size, container_size)
        self._set_view()
        self.refresh()

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

    def _get_children(self, model: model_type) -> List[model_type]:
        raise NotImplementedError

    def _refresh_rows(self) -> None:
        _rows_copy = {i.item.path: i.expanded for i in self._rows.values()}
        self._rows = {}

        def add_rows(item: Model, nest_level=0):

            name = item.name
            path = item.path

            def push_item(item: Model):
                expanded = _rows_copy.get(path, False)

                self._rows[name] = Component(
                    item,
                    nest_level,
                    len(self._rows),
                    expanded,
                )
                self._rows[name].index = len(self._rows) - 1

            if pattern := self.filter.value:
                description = getattr(item, "description")
                if re.findall(pattern, description):
                    push_item(item)
                for i in self._get_children(item):
                    add_rows(i, nest_level + 1)
            else:
                push_item(item)
                if self._rows[name].expanded:
                    for i in self._get_children(item):
                        add_rows(i, nest_level + 1)

        if self.model:
            for i in self._get_children(self.model):
                add_rows(i)

        self.row_vals: List[Component] = list(self._rows.values())
        self.refresh()

    async def change_status(self, status: StatusType):
        await self.emit(ChangeStatus(self, status))

    async def start_edit(self, field: str) -> None:
        if field == "none":
            return

        if not self.component:
            return

        if field not in self.component.fields.keys():
            await self.notify(
                f"[yellow]Can't change [b orange1]`{field}`[/b orange1] here![/yellow]"
            )
            return

        if field == "description":
            await self.change_status("INSERT")
        elif field == "tags":
            await self.change_status("TAG")
        elif field == "due":
            await self.change_status("DATE")

        if field == "tags":
            self.component.fields[field].value = getattr(self.item, f"{field}")
        else:
            self.component.fields[field].value = getattr(self.item, f"_{field}")

        self.component.fields[field].on_focus()
        self.editing = field

    async def _cancel_edit(self):
        await self.stop_edit(edit=False)

    async def stop_edit(self, edit: bool = True) -> None:
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

        await self.notify(res.text())
        if not res.ok:
            if res.cancel_op:
                await self.remove_item()
            await self._current_change_callback()
        else:
            self.commit()

        simple_input.on_blur()
        self.component.refresh()
        self.editing = "none"
        await self.change_status("NORMAL")

    async def start_search(self) -> None:
        self.filter.on_focus()
        await self.notify(self.filter.render())
        await self.change_status("SEARCH")

    async def stop_search(self) -> None:
        self.filter.clear()
        self._refresh_rows()
        await self.notify(self.filter.render())
        await self.change_status("NORMAL")

    def _drop(self, item: model_type) -> None:
        item = item or self.item
        if item:
            item.drop(self.model_kind)

    def _add_child(self) -> model_type:
        if self.item:
            return self.item.add_child(self.model_kind)
        else:
            return self.model.add_child(self.model_kind)

    def _add_sibling(self) -> model_type:
        if self.item and self.current >= 0:
            return self.item.add_sibling(self.model_kind)
        else:
            return self.model.add_child(self.model_kind)

    def _next_sibling(self) -> Optional[model_type]:
        if self.item:
            return self.item.next_sibling(self.model_kind)

    def _prev_sibling(self) -> Optional[model_type]:
        if self.item:
            return self.item.prev_sibling(self.model_kind)

    def _shift_down(self) -> None:
        if self.item:
            return self.item.shift_down(self.model_kind)

    def _shift_up(self) -> None:
        if self.item:
            return self.item.shift_up(self.model_kind)

    async def remove_item(self) -> None:
        if not self.item:
            return

        item = self.item
        self.current = min(self.current, len(self.row_vals) - 2)
        self._drop(item)
        self._refresh_rows()
        await self._current_change_callback()
        self.commit()
        self.refresh()

    async def add_child(self) -> None:

        if self.component and self.item:
            self.component.expand()

        self._add_child()
        self._refresh_rows()
        await self.move_down()
        await self.start_edit("description")

    async def add_sibling(self) -> None:

        if not self.item:
            child = self._add_child()
            self._refresh_rows()
            self.current = self._rows[child.name].index
            await self.start_edit("description")
            return

        self._add_sibling()
        self._refresh_rows()
        self.commit()
        await self.to_next_sibling("description")

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
            await self.start_edit(edit)

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
        if self.current > 0:
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
        if not parent:
            return

        if parent.name in self._rows:
            index = self._rows[parent.name].index
            self.current = index

            await self.toggle_expand()

    def sort(self, attr: str) -> None:
        if self.item:
            curr = self.item.name
            self.item.sort(self.model_kind, attr)
            self._refresh_rows()
            self.current = self._rows[curr].index
            self.commit()

    async def copy_text(self) -> None:
        if self.item:
            pyperclip.copy(self.item.description)
            await self.notify("[green]Description copied to clipboard![/]")
        else:
            await self.notify("[red]No item selected![/]")

    async def sort_menu_toggle(self) -> None:
        self.sort_menu.visible = True

    async def switch_pane(self) -> None:
        pass

    async def handle_key(self, event: events.Key) -> None:

        event.stop()
        key = (
            event.character
            if (event.character and (event.character in PRINTABLE))
            else event.key
        )

        if self.editing != "none":
            field = self.row_vals[self.current].fields[self.editing]

            if key == "escape":
                await self._cancel_edit()
            elif key == "enter":
                await self.stop_edit()
            else:
                await field.handle_keypress(key)

        else:

            if self.sort_menu.visible:
                await self.sort_menu.handle_key(key)

            elif self.filter.has_focus:
                await self.filter.handle_keypress(key)
                await self.notify(self.filter.render())
                self._refresh_rows()
                self.current = 0

            else:

                self.key_manager.attach_key(key)
                bind = self.key_manager.get_method()
                if bind:
                    await self.change_status("NORMAL")
                    if hasattr(self, bind.func):
                        func = getattr(self, bind.func)
                        await func(*bind.params)
                    else:
                        await self.notify(
                            "[yellow]Cannot perform this operation here![/yellow]"
                        )

        self.refresh()

    async def spawn_help(self):
        await self.emit(SpawnHelp(self))

    def add_row(self, row: Component, highlight: bool) -> None:  # noqa

        entry = []
        kwargs = {i: str(j.render()) for i, j in row.fields.items()}

        for column in self.COLS:
            res = self.styler.style(
                column, row.item, highlight, self.editing != "none", kwargs
            )
            entry.append(res)

        return self.push_row(entry, row.depth, highlight)

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

    def _setup_table(self, pointer: TextType = "") -> None:
        if isinstance(pointer, str):
            pointer = Text.from_markup(pointer)

        self.pointer = pointer
        self.table = Table.grid(expand=True)
        if width := len(pointer.plain):
            self.table.add_column("pointer", width=width)

    def make_table(self) -> None:
        self._setup_table()

        for i in self.view.range():
            try:
                self.add_row(self.row_vals[i], i == self.current)
            except:
                pass

    def push_row(self, row: List[Text], padding: int, pointer: bool) -> None:
        if row:
            if pointer:
                row.insert(0, self.pointer)
            else:
                row.insert(0, Text(len(self.pointer) * " "))

            if not hasattr(self, "pad_index"):
                self.pad_index = 0

                for i, j in enumerate(self.table.columns):
                    if j.header == "description":
                        self.pad_index = i
                        break

            if row:
                hint = Text("  " * padding)
                row[self.pad_index] = hint + row[self.pad_index]
                row[self.pad_index].highlight_regex(self.filter.value, style="b red")

            self.table.add_row(*row)

    def render(self) -> RenderableType:

        if self.sort_menu.visible:
            to_render = self.sort_menu.render()
        elif not self.row_vals:
            EMPTY = [
                Text.from_markup(text) if isinstance(text, str) else text
                for text in self.EMPTY
            ]
            to_render = Align.center(
                Group(
                    *[Align.center(i) for i in EMPTY],
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
            border_style=LIT if self._has_focus else DIM,
        )
