from typing import Union
from dooit.api.manager import Manager
from dooit.api.todo import Todo
from dooit.api.workspace import Workspace
from collections import defaultdict
from .base_tree import BaseTree

ModelType = Union[Todo, Workspace, Manager]


class ModelTree(BaseTree):
    DEFAULT_CSS = """
    ModelTree {
        height: 100%;
        width: 100%;
    }
    """

    def __init__(self, model: ModelType) -> None:
        super().__init__(id=self.__class__.__name__)
        self._model = model
        self.expaned = defaultdict(bool)

    @property
    def model(self):
        raise NotImplementedError

    def force_refresh(self) -> None:
        raise NotImplementedError

    def on_mount(self):
        self.force_refresh()

    def key_p(self):
        if self.highlighted is not None:
            self.notify(str(self.highlighted))
            self.toggle_expand()
