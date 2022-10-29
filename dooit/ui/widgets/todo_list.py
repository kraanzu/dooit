from typing import Optional
from rich.table import Table
from rich.text import Text
from textual import events


from .tree import TreeList
from ...api.todo import Todo
from ...ui.events.events import SwitchTab
from ...api import Workspace
from ...ui.widgets.sort_options import SortOptions
from ...utils.default_config import *


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

    @property
    def EMPTY(self):
        if self._assigned:
            arr = EMPTY_TODO
        else:
            arr = dashboard

        return [Text.from_markup(i) if isinstance(i, str) else i for i in arr]

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
    def item(self) -> Optional[Todo]:
        return self.item

    async def check_extra_keys(self, event: events.Key):

        key = event.key

        if key in "d":
            await self._start_edit("due")
        elif key in "+=":
            if self.component and self.item:
                self.item.increase_urgency()
                self.component.refresh_item("urgency")
        elif key in "_-":
            if self.component and self.item:
                self.item.decrease_urgency()
                self.component.refresh_item("urgency")

    # ##########################################

    def _stylize_urgency(self, item, highlight: bool = False) -> Text:
        icons = todos["urgency"]
        colors = ["green", "orange1", "yellow", "red"]
        colors = {i: j for i, j in enumerate(colors, 1)}
        style = "b " if highlight else "d "
        rank = int(item)
        return Text(icons[rank], style=style + colors[rank])

    def _stylize_due(self, item, highlight: bool = False) -> Text:
        fmt = todos["due"]

        if highlight:
            if self.editing == "none":
                text: str = fmt["highlight"]
            else:
                text: str = fmt["edit"]
        else:
            text: str = fmt["dim"]

        text = text.format(due=item)
        return Text.from_markup(text)

    def _stylize_desc(self, item, highlight: bool = False) -> Text:
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

    def add_row(self, row, highlight: bool) -> None:

        item = [str(i.render()) for i in row.get_field_values()]
        desc = self._stylize_desc(item[0], highlight)
        date = self._stylize_due(item[1], highlight)
        urgency = self._stylize_urgency(item[2], highlight)

        return self.push_row([desc, date, urgency], row.depth)

    # ##########################################

    def _add_sibling(self) -> Todo:
        if self.item:
            return self.item.add_sibling()
        else:
            return self.model.add_todo()

    def _add_child(self) -> Todo:
        if self._assigned and self.item:
            return self.item.add_child()
        else:
            return self.model.add_todo()

    def _drop(self) -> None:
        if self.item:
            self.item.drop()

    def _next_sibling(self) -> Optional[Todo]:
        if self.item:
            return self.item.next_sibling()

    def _prev_sibling(self) -> Optional[Todo]:
        if self.item:
            return self.item.prev_sibling()

    def _shift_down(self) -> None:
        if self.item:
            return self.item.shift_down()

    def _shift_up(self) -> None:
        if self.item:
            return self.item.shift_up()
