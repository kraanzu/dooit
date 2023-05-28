from typing import Iterator, List
from textual.containers import Horizontal
from textual.widget import Widget
from dooit.api.workspace import Workspace
from dooit.ui.widgets.inputs import Description
from dooit.ui.widgets.utils import Padding, Pointer
from .node import Node


class WorkspaceWidget(Node):
    ModelType = Workspace

    def _get_model_children(self) -> List[Workspace]:
        return self.model.workspaces

    def draw(self) -> Iterator[Widget]:
        with Horizontal():
            yield Pointer(self.pointer)
            yield Padding(self.model.nest_level)
            yield Description(model=self.model)
