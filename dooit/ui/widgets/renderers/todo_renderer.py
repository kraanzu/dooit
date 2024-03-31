from rich.console import RenderableType
from .base_renderer import BaseRenderer, Todo


class TodoRender(BaseRenderer):
    @property
    def model(self) -> Todo:
        if not isinstance(self._model, Todo):
            raise ValueError(f"Expected Todo, got {type(self._model)}")
        return self._model

    def make_renderable(self) -> RenderableType:
        return self.model.description
