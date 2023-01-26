from typing import List
from rich.table import Table
from rich.text import Text

from .tree import Component, TreeList
from ...api import Manager, Workspace
from ..events import TopicSelect, SwitchTab
from ...utils.conf_reader import Config

conf = Config()
EMPTY_NAVBAR = conf.get("EMPTY_NAVBAR")
func = conf.get("nav_item_style")


class NavBar(TreeList):
    """
    NavBar class to manage UI's navbar
    """

    options = Workspace.fields
    EMPTY = EMPTY_NAVBAR
    model_kind = "workspace"
    model_type = Workspace

    async def _current_change_callback(self) -> None:
        await self.emit(TopicSelect(self, self.item))

    async def _refresh_data(self):

        if not self.item or not self.component:
            self._refresh_rows()
        else:
            editing = self.editing
            path = self.item.path
            _old_val = ""

            if editing != "none":
                _old_val = self.component.fields[editing].value
                await self._stop_edit()

            self._refresh_rows()
            self.current = -1
            for i, j in enumerate(self.row_vals):
                if j.item.path == path:
                    self.current = i
                    if editing != "none":
                        self.component.fields[editing].value = _old_val
                        await self._start_edit(editing)
                    break

        await self._current_change_callback()

    def _setup_table(self) -> None:
        self.table = Table.grid(expand=True)
        self.table.add_column("desc")

    async def switch_tabs(self) -> None:
        if self.current == -1:
            return

        if self.filter.value:
            if self.item:
                await self._current_change_callback()

            await self._stop_filtering()
            self.current = -1

        await self.emit(SwitchTab(self))

    def add_row(self, row: Component, highlight: bool) -> None:

        entry = []
        kwargs = {i: str(j.render()) for i, j in row.fields.items()}
        res = func(row.item, highlight, self.editing != "none")

        if isinstance(res, str):
            res = res.format(**kwargs)
            res = Text.from_markup(res)
        elif isinstance(res, Text):
            res.plain = res.plain.format(**kwargs)
        else:
            res = Text(str(res))

        entry.append(res)
        return self.push_row(entry, row.depth)

    def _get_children(self, model: Manager) -> List[Workspace]:
        return model.workspaces
