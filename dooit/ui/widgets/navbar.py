from typing import Tuple
from rich.table import Table
from dooit.api.workspace import Workspace
from textual.events import Key

from dooit.ui.events.events import SwitchTab
from .tree import TreeList
from ..events import TopicSelect


class NavBar(TreeList):
    def _get_table(self) -> Table:
        table = Table.grid()
        table.add_column("about")
        return table

    def _check_valid(self, depth: int) -> Tuple[int, bool]:
        ok = depth < 2
        return depth, ok

    async def handle_tab(self):
        if self.current == -1 or not self.row_vals:
            return

        await self.emit(SwitchTab(self))

    async def add_child(self):
        if isinstance(self.item, Workspace):
            return await super().add_child()
        else:
            await self.emit(SwitchTab(self))
            await self.emit(Key(self, "a"))

    @property
    def current(self) -> int:
        return super().current

    @current.setter
    def current(self, value):
        value = min(max(0, value), len(self.row_vals) - 1)
        self._current = value
        self._fix_view()
        self.refresh()
        self.emit_no_wait(TopicSelect(self, self.item))
