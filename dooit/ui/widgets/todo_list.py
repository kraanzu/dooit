from rich.table import Table

from dooit.api.model import MaybeModel, Model

from ...ui.events.events import SwitchTab
from ...api.workspace import Workspace
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

    def _get_children(self, model: Workspace):
        if self._assigned:
            return model.todos
        return []

    async def handle_tab(self):
        await self.emit(SwitchTab(self))

    def update_table(self, model: Workspace):
        # if not model:
        #     return

        self._assigned = True
        self.model = model
        self.current = 0 if self._get_children(model) else -1
        self._refresh_rows()
        self.refresh()

    def _get_table(self) -> Table:
        table = Table.grid()
        table.add_column("about")
        table.add_column("due")
        table.add_column("urgency")
        return table

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
