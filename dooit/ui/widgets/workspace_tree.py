from typing import List
from dooit.ui.widgets.formatters.workspace_tree_formatter import WorkspaceFormatter
from dooit.utils.keybinder import KeyBinder

from .tree import TreeList
from ...api import Manager, Workspace
from ..events import TopicSelect, SwitchTab
from ...utils.conf_reader import Config

conf = Config()
EMPTY_WORKSPACE = conf.get("EMPTY_WORKSPACE")
format = conf.get("WORKSPACE")


class WorkspaceTree(TreeList):
    """
    NavBar class to manage UI's navbar
    """

    options = Workspace.fields
    EMPTY = EMPTY_WORKSPACE
    model_kind = "workspace"
    model_type = Workspace
    styler = WorkspaceFormatter(format)
    COLS = ["desc"]
    key_manager = KeyBinder()

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
                await self.stop_edit()

            self._refresh_rows()
            self.current = -1
            for i, j in enumerate(self.row_vals):
                if j.item.path == path:
                    self.current = i
                    if editing != "none":
                        self.component.fields[editing].value = _old_val
                        await self.start_edit(editing)
                    break

        await self._current_change_callback()

    def _setup_table(self) -> None:
        super()._setup_table(format["pointer"])
        self.table.add_column("desc", ratio=1)

    async def switch_tabs(self) -> None:
        if self.current == -1:
            return

        if self.filter.value:
            if self.item:
                await self._current_change_callback()

            await self.stop_search()
            self.current = -1

        await self.emit(SwitchTab(self))

    def _get_children(self, model: Manager) -> List[Workspace]:
        return model.workspaces
