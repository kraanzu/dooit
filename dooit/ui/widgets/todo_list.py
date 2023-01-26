from typing import Optional
from rich.table import Table
from rich.text import Text
from textual import events

from dooit.utils.conf_reader import Config

from .tree import Component, TreeList
from ...api.todo import Todo
from ...ui.events.events import SwitchTab
from ...api import Workspace

conf = Config()
EMPTY_TODO = conf.get("EMPTY_TODO")
dashboard = conf.get("dashboard")
todo_columns = conf.get("todo_columns")
PRINTABLE = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "


class TodoList(TreeList):
    """
    Tree structured Class to manage todos
    """

    options = Todo.fields
    EMPTY = dashboard
    model_kind = "todo"
    model_type = Todo

    def _get_children(self, model: Workspace):
        if model:
            return model.todos
        return []

    async def switch_tabs(self):
        if self.filter.value:
            await self._stop_filtering()

        await self.emit(SwitchTab(self))

    async def update_table(self, model: Optional[Workspace] = None):
        if not model:
            self.EMPTY = dashboard
            self.model = None
            self._refresh_rows()
        else:
            self.EMPTY = EMPTY_TODO
            if not self.item or not self.component:
                self.model = model
                self.current = -1
                self._refresh_rows()
            else:
                editing = self.editing
                path = self.item.path
                _old_val = ""

                if editing != "none":
                    _old_val = self.component.fields[editing].value
                    await self._cancel_edit()

                self.model = model
                self._refresh_rows()

                self.current = -1
                for i, j in enumerate(self.row_vals):
                    if j.item.path == path:
                        self.current = i
                        if editing != "none":
                            self.component.fields[editing].value = _old_val
                            await self.component.fields[editing].handle_keypress("end")
                            await self._start_edit(editing)
                        break

        self.refresh()

    def _setup_table(self) -> None:
        self.table = Table.grid(expand=True)
        for name, item in todo_columns.items():
            self.table.add_column(name, ratio=item[0])

    # ##########################################

    async def check_extra_keys(self, event: events.Key):

        key = (
            event.character
            if (event.character and (event.character in PRINTABLE))
            else event.key
        )

        if self.editing != "none":
            return
        if key in "d":
            await self._start_edit("due")
        elif key in "e":
            await self._start_edit("eta")
        elif key in "t":
            await self._start_edit("tags")
        elif key in "r":
            await self._start_edit("recur")
        elif key in "c":
            if self.item and self.component:
                self.item.toggle_complete()
                self.component.refresh_item("status")
                self.component.refresh_item("due")
        elif key in "+=":
            if self.component and self.item:
                self.item.increase_urgency()
                self.component.refresh_item("urgency")
        elif key in "_-":
            if self.component and self.item:
                self.item.decrease_urgency()
                self.component.refresh_item("urgency")

    def add_row(self, row: Component, highlight: bool) -> None:

        entry = []
        kwargs = {i: str(j.render()) for i, j in row.fields.items()}

        for _, func in todo_columns.values():
            res = func(
                row.item,
                highlight,
                self.editing != "none",
            )
            if isinstance(res, str):
                res = res.format(**kwargs)
                res = Text.from_markup(res)
            else:
                res.plain = res.plain.format(**kwargs)
            entry.append(res)

        return self.push_row(entry, row.depth)
