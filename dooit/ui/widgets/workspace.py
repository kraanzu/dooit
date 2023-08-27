from typing import Iterator, List
from textual.widget import Widget
from dooit.api.workspace import Workspace
from dooit.ui.widgets.inputs import Description
from dooit.ui.widgets.utils import Padding
from dooit.utils.conf_reader import config_man
from .node import Node

EDITING = config_man.get("WORKSPACE").get("editing")
POINTER_ICON = config_man.get("WORKSPACE").get("pointer")


class WorkspaceGrid(Widget):
    DEFAULT_CSS = f"""
    WorkspaceGrid {{
        layout: grid;
        grid-size: 3;
        grid-columns: auto auto 1fr;
        height: auto;
    }}

    WorkspaceGrid > Description.editing {{
        color: {EDITING};
    }}
    """


class WorkspaceWidget(Node):
    """
    Subclass of `Node` class to visualize workspace
    """

    ModelType = Workspace
    pointer_icon = POINTER_ICON

    def setup_children(self) -> None:
        self.description = Description(self.model)

    def _get_model_children(self) -> List[Workspace]:
        return self.model.workspaces

    def draw(self) -> Iterator[Widget]:
        with WorkspaceGrid():
            yield self.pointer
            yield Padding(self.model.nest_level)
            yield self.description
