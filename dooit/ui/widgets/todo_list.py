from rich.table import Table

from dooit.api.model import Model

from dooit.api.workspace import Workspace
from .tree import TreeList


class TodoList(TreeList):
    def __init__(self):
        super().__init__()
        self._assigned = False

    def make_table(self):
        if not self._assigned:
            self.table = Table.grid()
        else:
            super().make_table()
    
    def _get_children(self, model: Model):
        if self._assigned:
            return model.get_todos()
        return []

    def update_table(self, model: Model):

        if isinstance(model, Workspace): # common topic
            model = model.topic

        self._assigned = True
        self.model = model
        self.current = -1
        self._refresh_rows()
        self.refresh()

    def _get_table(self) -> Table:
        table = Table.grid()
        table.add_column("about")
        table.add_column("due")
        table.add_column("urgency")
        return table
