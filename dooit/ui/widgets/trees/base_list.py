from typing import Iterable, Optional, Union
from textual.widgets import OptionList
from textual.widgets.option_list import Option
from dooit.api.todo import Todo
from dooit.api.workspace import Workspace
from collections import defaultdict

ModelType = Union[Todo, Workspace]


class BaseList(OptionList):
    expanded_nodes = defaultdict(bool)

    def _insert_nodes(self, index: int, items: Iterable[Option]) -> None:
        if items:
            content = [self._make_content(item) for item in items]
            options = [item for item in content if isinstance(item, Option)]

            self._duplicate_id_check(content)

            self._contents = self._contents[:index] + content + self._contents[index:]
            self._options = self._options[:index] + options + self._options[index:]

            self._refresh_content_tracking(force=True)
            self.refresh()

    def add_nodes(self, *items: Option, index: Optional[int] = None) -> None:
        if index is None:
            index = self.option_count

        self._insert_nodes(index, items)

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

        self.expanded_nodes[node.id] = True
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
