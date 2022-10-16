from rich.table import Table

from dooit.api.model import MaybeModel

from ...api.manager import Manager, Model
# from ...api.workspace import Workspace
from .tree import TreeList
from ..events import TopicSelect, SwitchTab


class NavBar(TreeList):
    def _get_table(self) -> Table:
        table = Table.grid()
        table.add_column("about")
        return table

    async def handle_tab(self):
        if self.current == -1:
            return

        await self.emit(SwitchTab(self))

    @property
    def current(self) -> int:
        return super().current

    @current.setter
    def current(self, value):
        value = min(max(0, value), len(self.row_vals) - 1)
        self._current = value
        self._fix_view()
        self.refresh()
        if self.item:
            self.emit_no_wait(TopicSelect(self, self.item))

    # ##########################################
    
    def _get_children(self, model: Manager):
        return model.workspaces

    def _add_sibling(self):
        if self.item and self.current >= 0:
            self.item.add_sibling_workspace()
        else:
            self.model.add_child_workspace()

    def _add_child(self) -> Model:
        if self.item:
            return self.item.add_child_workspace()
        else:
            return self.model.add_child_workspace()

    def _drop(self):
        if self.item:
            self.item.drop_workspace()

    def _next_sibling(self) -> MaybeModel:
        if self.item:
            return self.item.next_workspace()

    def _prev_sibling(self) -> MaybeModel:
        if self.item:
            return self.item.prev_workspace()

    def _shift_down(self):
        if self.item:
            return self.item.shift_workspace_down()

    def _shift_up(self):
        if self.item:
            return self.item.shift_workspace_up()
