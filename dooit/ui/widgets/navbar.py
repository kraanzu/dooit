from typing import List, Optional
from rich.table import Table
from rich.text import Text

from .tree import Component, TreeList
from ...ui.widgets.sort_options import SortOptions
from ...api import Manager, Model, Workspace
from ..events import TopicSelect, SwitchTab
from ...utils.default_config import *  # noqa


class NavBar(TreeList):
    """
    NavBar class to manage UI's navbar
    """

    def __init__(self):
        super().__init__()
        self.sort_menu = SortOptions(
            name=f"Sort_{self.name}", options=Workspace.fields, parent_widget=self
        )
        self.sort_menu.visible = False

    @property
    def EMPTY(self):
        return [Text.from_markup(i) if isinstance(i, str) else i for i in EMPTY_NAVBAR]

    @property
    def item(self) -> Optional[Workspace]:
        if self.component:
            return self.component.item

    async def _refresh_data(self):

        if not self.item:
            self._refresh_rows()
        else:
            editing = self.editing
            path = self.item.path

            if editing != "none":
                await self._stop_edit()

            self._refresh_rows()
            index = 0 if self.row_vals else -1
            for i, j in enumerate(self.row_vals):
                if j.item.path == path:
                    index = i
                    break

            self.current = index
            if editing != "none":
                await self._start_edit(editing)

    def _setup_table(self) -> None:
        self.table = Table.grid(expand=True)
        self.table.add_column("desc")

    async def handle_tab(self) -> None:
        if self.current == -1:
            return

        if self.filter.value:

            if self.item:
                await self.emit(
                    TopicSelect(
                        self,
                        self.item,
                    )
                )

            await self._stop_filtering()
            self.current = -1

        await self.emit(SwitchTab(self))

    async def watch_current(self, value: int) -> None:

        value = min(value, len(self.row_vals) - 1)
        self.current = value

        self._fix_view()
        if self.current != -1 and self.item:
            await self.emit(TopicSelect(self, self.item))

        self.refresh()

    def add_row(self, row: Component, highlight: bool) -> None:

        kwargs = {i: str(j.render()) for i, j in row.fields.items()}
        desc = self._stylize(navbar["desc"], highlight, kwargs)
        return self.push_row([desc], row.depth)

    def _get_children(self, model: Manager) -> List[Workspace]:
        return model.workspaces

    def _add_sibling(self):
        if self.item and self.current >= 0:
            self.item.add_sibling()
        else:
            self.model.add_child_workspace()

    def _add_child(self) -> Model:
        if self.item:
            return self.item.add_workspace()
        else:
            return self.model.add_child_workspace()

    def _drop(self, item: Optional[Workspace] = None) -> None:

        item = item or self.item
        if item:
            item.drop()

    def _next_sibling(self) -> Optional[Model]:
        if self.item:
            return self.item.next_sibling()

    def _prev_sibling(self) -> Optional[Model]:
        if self.item:
            return self.item.prev_sibling()

    def _shift_down(self) -> None:
        if self.item:
            return self.item.shift_down()

    def _shift_up(self) -> None:
        if self.item:
            return self.item.shift_up()
