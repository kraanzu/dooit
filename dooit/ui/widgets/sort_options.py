from typing import Optional, Type, Union
from rich.console import RenderableType
from rich.table import Table
from rich.text import Text
from textual.app import ComposeResult
from textual.widget import Widget
from dooit.api.todo import Todo
from dooit.api.workspace import Workspace
from dooit.ui.events import ApplySortMethod, ChangeStatus, Notify
from dooit.utils import KeyBinder
from textual.widgets import Label


class SortOptions(Widget):
    """
    A list class to show and select the items in a list
    """

    key_manager = KeyBinder()

    def __init__(
        self,
        model_type: Union[Type[Workspace], Type[Todo]],
        model: Union[Workspace, Todo],
    ) -> None:
        super().__init__(classes="no-border")
        self.model_type = model_type
        self.model = model
        self.options = model_type.sortable_fields
        self.model_widget = model
        self.highlighted = 0

    def highlight(self, id: int) -> None:
        self.highlighted = id
        self.refresh(layout=True)

    def hide(self) -> None:
        self.visible = False

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
        await self.send_message(ChangeStatus, "NORMAL")
        self.visible = False

    def sort(self, method: str):
        self.model_widget

    async def keypress(self, key: str) -> None:
        if key == "escape":
            await self.parent.sort_menu_toggle()
            return

        if key == "enter":
            option = self.options[self.highlighted]
            await self.parent.apply_sort(option)
            # await self.parent.sort_menu_toggle()
            return

        self.key_manager.attach_key(key)
        bind = self.key_manager.get_method()
        if bind:
            if hasattr(self, bind.func_name):
                func = getattr(self, bind.func_name)
                await func(*bind.params)
            else:
                self.post_message(
                    Notify("[yellow]No such operation for sort menu![/yellow]")
                )

        self.refresh()

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
