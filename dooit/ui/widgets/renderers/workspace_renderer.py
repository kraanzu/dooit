from rich.console import RenderableType
from .base_renderer import BaseRenderer, Workspace
from dooit.ui.widgets.inputs.inputs import WorkspaceDescription


class WorkspaceRender(BaseRenderer):
    @property
    def model(self) -> Workspace:
        if not isinstance(self._model, Workspace):
            raise ValueError(f"Expected Workspace, got {type(self._model)}")
        return self._model

    def post_init(self):
        self.description = WorkspaceDescription(self.model)

    @property
    def prompt(self) -> RenderableType:
        return self.description.render()

    def start_edit(self, param: str):
        self.description.start_edit()
