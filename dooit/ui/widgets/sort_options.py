from typing import Type, Union
from rich.console import RenderableType
from rich.table import Table
from rich.text import Text
from textual.widget import Widget
from dooit.api.todo import Todo
from dooit.api.workspace import Workspace
from dooit.ui.events import ChangeStatus
from dooit.ui.events.events import ApplySort
from dooit.ui.widgets.kwidget import KeyWidget


class SortOptions(KeyWidget, Widget):
    """
    A list class to show and select the items in a list
    """

    DEFAULT_CSS = """
    SortOptions {
        layer: L1;
        visibility: hidden;
    }
    """

    def __init__(self, model_type: Union[Type[Workspace], Type[Todo]]) -> None:
        super().__init__(classes="no-border")
        self.model_type = model_type
        self.options = model_type.sortable_fields
        self.highlighted = 0
        self._prev_highlighted = 0
        self.add_keys(
            {
                "cancel_sort": "<escape>",
                "stop": "<enter>",
            }
        )

    @property
    def selected_option(self):
        return self.options[self.highlighted]

    def set_id(self, widget_id: str):
        self.widget_id = widget_id

    def highlight(self, id: int) -> None:
        self.highlighted = id
        self.refresh(layout=True)

    def hide(self):
        self.styles.layer = "L1"
        self.styles.visibility = "hidden"

    async def start(self):
        self.styles.layer = "L4"
        self.styles.visibility = "visible"
        self._prev_highlighted = self.highlighted
        self.post_message(ChangeStatus("SORT"))

    async def stop(self):
        self.hide()
        if self.model_type == Workspace:
            query = "WorkspaceTree"
        else:
            query = "TodoTree.current"

        self.post_message(ApplySort(query, self.widget_id, self.selected_option))
        self.post_message(ChangeStatus("NORMAL"))

    async def toggle_visibility(self):
        if self.visible:
            await self.stop()
        else:
            await self.start()

    async def move_down(self) -> None:
        """
        Moves the highlight down
        """

        self.highlight(min(self.highlighted + 1, len(self.options) - 1))

    async def move_up(self) -> None:
        """
        Moves the highlight up
        """

        self.highlight(max(self.highlighted - 1, 0))

    async def move_to_top(self) -> None:
        """
        Moves the cursor to the top
        """
        self.highlight(0)

    async def move_to_bottom(self) -> None:
        """
        Moves the cursor to the bottom
        """

        self.highlight(len(self.options) - 1)

    async def sort_menu_toggle(self):
        self.visible = False

    async def cancel_sort(self):
        self.highlighted = self._prev_highlighted
        self.hide()

    def add_option(self, option: str) -> None:
        self.options.append(option)
        self.refresh()

    def render(self) -> RenderableType:
        table = Table.grid()
        table.add_column("")

        for index, option in enumerate(self.options):
            if index != self.highlighted:
                option = "  " + option
                style = "dim"
            else:
                option = "> " + option
                style = "bold"

            label = Text(option, style)
            label = Text("  ") + label
            table.add_row(label)

        return table
