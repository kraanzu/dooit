from typing import TYPE_CHECKING

from rich.table import Table

from dooit.api.workspace import Workspace


if TYPE_CHECKING:
    from dooit.ui.api.components import WorkspaceLayout


class Registry:
    """
    Class to store global variables and objects
    """

    def __init__(self) -> None:
        self.workspace_layout = []

    def set_workspace_layout(self, layout: "WorkspaceLayout"):
        self.workspace_layout = layout

    def get_workspace_layout(self) -> "WorkspaceLayout":
        return self.workspace_layout

    def get_workspace_table(self, workspace: Workspace) -> Table:

        def get_max(items, property, formatter):
            #TODO: OPTIMIZE THIS !!!
            values = [getattr(item, property) for item in items]

            return max(
                [len(formatter(value)) for value in values]
                + [len(value) for value in values]
            )

        table = Table.grid(expand=True)
        layout = self.get_workspace_layout()

        for column, formatter in layout:
            if column.value == "description":
                table.add_column(column.value, ratio=1)
            else:
                table.add_column(
                    column.value,
                    width=get_max(
                        workspace.workspaces,
                        column.value,
                        formatter,
                    ),
                )

        return table


registry = Registry()
