from typing import Tuple
from rich.table import Table
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
