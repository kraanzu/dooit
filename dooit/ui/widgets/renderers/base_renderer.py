from typing import Union
from rich.console import RenderableType
from textual.widgets.option_list import Option
from dooit.api.todo import Todo
from dooit.api.workspace import Workspace

ModelType = Union[Todo, Workspace]


class BaseRenderer(Option):
    editing: str = ""

    def __init__(self, model: ModelType):
        self._model = model
        super().__init__("", id=model.uuid)
        self.post_init()

    def post_init(self):
        pass

    @property
    def model(self) -> ModelType:
        raise NotImplementedError

    def make_renderable(self) -> RenderableType:
        raise NotImplementedError

    def start_edit(self, param: str) -> bool:
        if not hasattr(self, param):
            return False

        getattr(self, param).start_edit()
        self.editing = param
        return True

    def stop_edit(self):
        getattr(self, self.editing).stop_edit()
        self.editing = ""

    def handle_key(self, event) -> bool:
        return True
