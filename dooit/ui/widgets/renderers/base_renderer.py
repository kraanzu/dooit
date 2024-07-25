from typing import Any, Callable, Dict, Optional, Union
from rich.console import RenderableType
from textual.app import events
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
    def table_layout(self) -> Any:
        raise NotImplementedError

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

    def handle_key(self, event: events.Key) -> bool:
        getattr(self, self.editing).keypress(event.key)
        return True

    def refresh_prompt(self) -> None:
        self.set_prompt(self.make_renderable())
