from rich.console import RenderableType
from .base_renderer import BaseRenderer, Workspace


class WorkspaceRender(BaseRenderer):
    @property
    def model(self) -> Workspace:
        return self._model

    def make_renderable(self) -> RenderableType:
        return self.model.description
