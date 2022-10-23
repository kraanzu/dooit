from ctypes.wintypes import WORD
from rich.table import Table
from rich.text import Text
from dooit.api.workspace import Workspace

from dooit.ui.widgets.sort_options import SortOptions

from ...api.model import MaybeModel
from ...api.manager import WORKSPACE, Manager, Model
from .tree import TreeList
from ..events import TopicSelect, SwitchTab
from dooit.utils.default_config import navbar


class NavBar(TreeList):
    def __init__(self):
        super().__init__()
        self.sort_menu = SortOptions(
            name=f"Sort_{self.name}",
            options=Workspace.fields,
            parent_widget=self
        )
        self.sort_menu.visible = False

    def set_styles(self):
        self.style_on = navbar["about"]["highlight"]
        self.style_off = navbar["about"]["dim"]
        self.style_edit = navbar["about"]["edit"]

    def _setup_table(self) -> None:
        self.table = Table.grid(expand=True)
        self.table.add_column("about")

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

    def add_row(self, row, highlight: bool):
        padding = "  " * row.depth
        items = [str(i.render()) for i in row.get_field_values()]
        desc = Text(padding) + self._stylize_desc(items[0], highlight)

        self.table.add_row(desc)

    # ##########################################

    def _stylize_desc(self, item, highlight: bool = False) -> Text:
        fmt = navbar["about"]

        if highlight:
            if self.editing == "none":
                text: str = fmt["highlight"]
            else:
                text: str = fmt["edit"]
        else:
            text: str = fmt["dim"]

        text = text.format(desc=item)
        return Text.from_markup(text)

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
