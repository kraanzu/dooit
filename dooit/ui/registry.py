from typing import TYPE_CHECKING, Callable, List

from rich.table import Table
from dooit.api.model import DooitModel
from dooit.api.workspace import Workspace


if TYPE_CHECKING:
    from dooit.ui.api.components import WorkspaceLayout, TodoLayout


class Registry:
    """
    Class to store global variables and objects
    """

    def __init__(self) -> None:
        self.workspace_layout = []
        self.todo_layout = []

    def __get_max_column_width(self, items: List, property: str, formatter: Callable):
        # TODO: OPTIMIZE THIS !!!

        values = [getattr(item, property) for item in items]

        return max(
            [len(formatter(getattr(item, property), item)) for item in items]
            + [len(value) for value in values]
        )

    def __create_table_from_layout(self, layout, items):
        table = Table.grid(expand=True)

        for column, formatter in layout:
            if column.value == "description":
                table.add_column(column.value, ratio=1)
            else:
                table.add_column(
                    column.value,
                    width=self.__get_max_column_width(
                        items,
                        column.value,
                        formatter,
                    ),
                )

        return table

    def set_workspace_layout(self, layout: "WorkspaceLayout"):
        layout = [
            item if isinstance(item, tuple) else (item, lambda value, _: value)
            for item in layout
        ]
        self.workspace_layout = layout

    def get_workspace_layout(self) -> "WorkspaceLayout":
        return self.workspace_layout

    def set_todo_layout(self, layout: "TodoLayout"):
        layout = [
            (
                item
                if isinstance(item, tuple)
                else (
                    item,
                    lambda value, _: value,
                )
            )
            for item in layout
        ]
        self.todo_layout = layout

    def get_todo_layout(self) -> "TodoLayout":
        return self.todo_layout

    def get_todo_table(self, model: DooitModel) -> Table:
        layout = self.get_todo_layout()
        items = model.todos

        return self.__create_table_from_layout(layout, items)

    def get_workspace_table(self, workspace: Workspace) -> Table:

        layout = self.get_workspace_layout()
        items = workspace.workspaces

        return self.__create_table_from_layout(layout, items)


registry = Registry()
