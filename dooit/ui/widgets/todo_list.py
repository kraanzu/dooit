from typing import Tuple
from rich.table import Table
from .tree import TreeList


class TodoList(TreeList):
    def _get_table(self) -> Table:
        table = Table.grid()
        table.add_column("about")
        table.add_column("due")
        table.add_column("urgency")
        return table

    def _check_valid(self, depth: int) -> Tuple[int, bool]:
        ok = depth > 2
        return depth - 2, ok
