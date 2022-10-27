from typing import Union
from rich.table import Table
from rich.text import Text
from textual import events

from dooit.ui.widgets.sort_options import SortOptions

from ...api.todo import Todo
from ...api.model import MaybeModel, Model
from ...ui.events.events import SwitchTab
from ...api.workspace import Workspace
from .tree import TreeList
from dooit.utils import default_config

todos = default_config.todos


class TodoList(TreeList):
    def __init__(self):
        super().__init__()
        self._assigned = False
        self.sort_menu = SortOptions(
            name=f"Sort_{self.name}",
            options=Todo.fields,
            parent_widget=self,
        )
        self.sort_menu.visible = False

    async def watch_current(self, value: int):
        if not self.row_vals:
            self.current = -1
        else:
            value = min(max(0, value), len(self.row_vals) - 1)
            self.current = value
            self._fix_view()

        self.refresh()

    def make_table(self):
        if not self._assigned:
            self.table = Table.grid()
        else:
            super().make_table()

    def _get_children(self, model: Workspace):
        if self._assigned and model:
            return model.todos
        return []

    async def handle_tab(self):
        if self.filter.value:
            await self._stop_filtering()

        await self.emit(SwitchTab(self))

    def update_table(self, model: Workspace):
        self._assigned = True
        self.model = model
        self.current = 0 if self._get_children(model) else -1
        self._refresh_rows()
        self.refresh()

    def _setup_table(self) -> None:
        self.table = Table.grid(expand=True)
        self.table.add_column("about", ratio=80)
        self.table.add_column("due", ratio=15)
        self.table.add_column("urgency", ratio=5)

    # ##########################################

    @property
    def item(self) -> Union[Todo, None]:
        return super().item

    async def check_extra_keys(self, event: events.Key):
        match event.key:
            case "d":
                await self._start_edit("due")
            case "+" | "=":
                if self.component and self.item:
                    self.item.increase_urgency()
                    self.component.refresh_item("urgency")
            case "-" | "_":
                if self.component and self.item:
                    self.item.decrease_urgency()
                    self.component.refresh_item("urgency")

    # ##########################################

    def _stylize_urgency(self, item, highlight: bool = False):
        icons = todos["urgency"]
        colors = ["green", "orange1", "yellow", "red"]
        colors = {i: j for i, j in enumerate(colors, 1)}
        style = "b " if highlight else "d "
        rank = int(item)
        return Text(icons[rank], style=style + colors[rank])

    def _stylize_date(self, item, highlight: bool = False):
        fmt = todos["date"]

        if highlight:
            if self.editing == "none":
                text: str = fmt["highlight"]
            else:
                text: str = fmt["edit"]
        else:
            text: str = fmt["dim"]

        text = text.format(date=item)
        return Text.from_markup(text)

    def _stylize_desc(self, item, highlight: bool = False):
        fmt = todos["about"]

        if highlight:
            if self.editing == "none":
                text: str = fmt["highlight"]
            else:
                text: str = fmt["edit"]
        else:
            text: str = fmt["dim"]

        text = text.format(desc=item)
        return Text.from_markup(text)

    def add_row(self, row, highlight: bool):

        # padding = "  " * row.depth
        item = [str(i.render()) for i in row.get_field_values()]
        desc = self._stylize_desc(item[0], highlight)
        date = self._stylize_date(item[1], highlight)
        urgency = self._stylize_urgency(item[2], highlight)

        self.push_row([desc, date, urgency], row.depth)
        # self.table.add_row(desc, date, urgency)

    # ##########################################

    def _add_sibling(self) -> Model:
        if self.item:
            return self.item.add_sibling_todo()
        else:
            return self.model.add_child_todo()

    def _add_child(self) -> Model:
        if self._assigned and self.item:
            return self.item.add_child_todo()
        else:
            return self.model.add_child_todo()

    def _drop(self):
        if self.item:
            self.item.drop_todo()

    def _next_sibling(self) -> MaybeModel:
        if self.item:
            return self.item.next_todo()

    def _prev_sibling(self) -> MaybeModel:
        if self.item:
            return self.item.prev_todo()

    def _shift_down(self):
        if self.item:
            return self.item.shift_todo_down()

    def _shift_up(self):
        if self.item:
            return self.item.shift_todo_up()
