from rich.console import RenderableType
from rich.table import Table

from dooit.api.model import Model
from .tree import TreeList


class TodoList(TreeList):
    def __init__(self):
        super().__init__()
        self._assigned = False

    def make_table(self):
        if not self._assigned:
            self.table = Table.grid()
            return

        return super().make_table()

    def update_table(self, model: Model):
        self._assigned = True
        self.model = model
        self._refresh_rows()
        self.refresh()

    def _get_table(self) -> Table:
        table = Table.grid()
        table.add_column("about")
        table.add_column("due")
        table.add_column("urgency")
        return table
