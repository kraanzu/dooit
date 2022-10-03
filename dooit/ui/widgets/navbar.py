from typing import Tuple
from rich.table import Table
from .tree import TreeList


class NavBar(TreeList):
    def _get_table(self) -> Table:
        table = Table.grid()
        table.add_column("about")
        return table

    def _check_valid(self, depth: int) -> Tuple[int, bool]:
        ok = depth < 2
        return depth, ok
