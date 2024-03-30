from rich.console import RenderableType
from .base_renderer import BaseRenderer, Todo


class TodoRender(BaseRenderer):
    @property
    def model(self) -> Todo:
        return self._model

    def make_renderable(self) -> RenderableType:
        return self.model.description
