from typing import List
from .base_renderer import BaseRenderer, Workspace
from ..inputs.model_inputs import WorkspaceDescription
from ...registry import registry


class WorkspaceRender(BaseRenderer):
    @property
    def model(self) -> Workspace:
        if not isinstance(self._model, Workspace):
            raise ValueError(f"Expected Workspace, got {type(self._model)}")
        return self._model

    @property
    def table_layout(self) -> List:
        return registry.get_workspace_layout()

    def post_init(self):
        self.description = WorkspaceDescription(self.model)
