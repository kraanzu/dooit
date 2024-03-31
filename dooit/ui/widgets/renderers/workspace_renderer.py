from rich.console import RenderableType
from .base_renderer import BaseRenderer, Workspace


class WorkspaceRender(BaseRenderer):
    @property
    def model(self) -> Workspace:
        if not isinstance(self._model, Workspace):
            raise ValueError(f"Expected Workspace, got {type(self._model)}")
        return self._model

    def make_renderable(self) -> RenderableType:
        return self.model.description
