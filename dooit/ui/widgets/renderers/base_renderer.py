from typing import Union
from rich.console import RenderableType
from textual.widgets.option_list import Option

from dooit.api.model import Model
from dooit.api.todo import Todo
from dooit.api.workspace import Workspace


class BaseRenderer(Option):
    def __init__(self, model: Model):
        self._model = model
        super().__init__(self.make_renderable(), id=model.uuid)

    @property
    def model(self) -> Union[Todo, Workspace]:
        raise NotImplementedError

    def make_renderable(self) -> RenderableType:
        raise NotImplementedError
