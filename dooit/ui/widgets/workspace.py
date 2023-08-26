from typing import Iterator, List
from textual.widget import Widget
from dooit.api.workspace import Workspace
from dooit.ui.widgets.inputs import Description
from dooit.ui.widgets.utils import Padding
from dooit.utils.conf_reader import config_man
from .node import Node

EDITING = config_man.get("WORKSPACE").get("editing")


class WorkspaceWidget(Node):
    """
    Subclass of `Node` class to visualize workspace
    """

    DEFAULT_CSS = f"""
    WorkspaceWidget {{
        layout: grid;
        grid-size: 3;
        grid-columns: auto auto 1fr;
    }}

    WorkspaceWidget > Description.editing {{
        color: {EDITING};
    }}
    """

    ModelType = Workspace

    def setup_children(self) -> None:
        self.description = Description(self.model)

    def _get_model_children(self) -> List[Workspace]:
        return self.model.workspaces

    def draw(self) -> Iterator[Widget]:
        yield self.pointer
        yield Padding(self.model.nest_level)
        yield self.description
