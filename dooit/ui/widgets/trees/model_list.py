from typing import List, Union
from textual.widgets import OptionList
from textual.widgets.option_list import Option
from dooit.api.todo import Todo
from dooit.api.workspace import Workspace
from collections import defaultdict
from .base_list import BaseList

ModelType = Union[Todo, Workspace]


class ModelList(BaseList):
    def __init__(self, model: ModelType) -> None:
        super().__init__()
        self._model = model
        self.expaned = defaultdict(bool)

    @property
    def model(self):
        raise NotImplementedError

    @property
    def current_node(self) -> Option:
        if self.highlighted is None:
            raise ValueError("No node is currently highlighted")

        return self.get_option_at_index(self.highlighted)

    def expand_node(self) -> None:
        node = self.current_node
        index = self.highlighted

        if index is None:
            raise ValueError("No node is currently highlighted")

        if not node.id:
            raise ValueError("Node has no id")

        self.expaned[node.id] = True
        options = self._get_children(node.id)
        self._insert_nodes(index + 1, options)

    def collapse_node(self) -> None:
        node = self.current_node
        index = self.highlighted

        if index is None:
            raise ValueError("No node is currently highlighted")

        if not node.id:
            raise ValueError("Node has no id")

        self.expaned[node.id] = False
        children = self._get_children(node.id)
        for child in children:
            if _id := child.id:
                self.remove_option(_id)

    def toggle_expand(self) -> None:
        if self.highlighted is None:
            return

        expanded = self.expaned[self.current_node.id]
        if expanded:
            self.collapse_node()
        else:
            self.expand_node()

    def _get_children(self, id: str) -> List[Option]:
        raise NotImplementedError

    def force_refresh(self) -> None:
        raise NotImplementedError

    def on_mount(self):
        self.force_refresh()

    def key_p(self):
        if self.highlighted is not None:
            self.notify(str(self.highlighted))
            self.toggle_expand()
