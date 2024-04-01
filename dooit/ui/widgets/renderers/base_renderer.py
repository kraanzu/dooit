from typing import Union
from rich.console import RenderableType
from textual.widgets.option_list import Option
from dooit.api.todo import Todo
from dooit.api.workspace import Workspace

ModelType = Union[Todo, Workspace]

class BaseRenderer(Option):
    def __init__(self, model: ModelType):
        self._model = model
        super().__init__(self.make_renderable(), id=model.uuid)

    @property
    def model(self) -> ModelType:
        raise NotImplementedError

    def make_renderable(self) -> RenderableType:
        raise NotImplementedError
