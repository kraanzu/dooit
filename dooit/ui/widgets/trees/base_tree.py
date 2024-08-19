from typing import TYPE_CHECKING, Iterable, Optional, Union
from textual.widgets import OptionList
from textual.widgets.option_list import Option
from dooit.api.todo import Todo
from dooit.api.workspace import Workspace
from collections import defaultdict

ModelType = Union[Todo, Workspace]

if TYPE_CHECKING:
    from ....ui.tui import Dooit


class BaseTree(OptionList, can_focus=True, inherit_bindings=False):
    expanded_nodes = defaultdict(bool)

    @property
    def tui(self) -> "Dooit":
        from ....ui.tui import Dooit

        if isinstance(self.app, Dooit):
            return self.app

        raise ValueError("App is not a Dooit instance")

    @property
    def node(self) -> Option:
        if self.highlighted is None:
            raise ValueError("No node is currently highlighted")

        return self.get_option_at_index(self.highlighted)

    def _get_parent(self, id: str) -> Optional[Option]:
        raise NotImplementedError

    def _get_children(self, id: str) -> Iterable[Option]:
        raise NotImplementedError

    def _insert_nodes(self, index: int, items: Iterable[Option]) -> None:
        if items:
            content = [self._make_content(item) for item in items]
            options = [item for item in content if isinstance(item, Option)]

            self._duplicate_id_check(content)

            self._contents = self._contents[:index] + content + self._contents[index:]
            self._options = self._options[:index] + options + self._options[index:]

            self.refresh_options()

    def add_nodes(self, *items: Option, index: Optional[int] = None) -> None:
        if index is None:
            index = self.option_count

        self._insert_nodes(index, items)

    def _expand_node(self, _id: str) -> None:
        self.expanded_nodes[_id] = True
        options = self._get_children(_id)
        index = self.get_option_index(_id)
        self._insert_nodes(index + 1, options)

    def expand_node(self) -> None:
        if self.highlighted is not None and self.node.id:
            self._expand_node(self.node.id)

    def _collapse_node(self, _id: str) -> None:
        self.expanded_nodes[_id] = False
        children = self._get_children(_id)
        for child in children:
            if child_id := child.id:
                self.remove_option(child_id)

    def collapse_node(self) -> None:
        if self.node.id:
            self._collapse_node(self.node.id)

    def _toggle_expand_node(self, _id: str) -> None:
        expanded = self.expanded_nodes[_id]
        if expanded:
            self._collapse_node(_id)
        else:
            self._expand_node(_id)

    def toggle_expand(self) -> None:
        if self.highlighted is None or not self.node.id:
            return

        self._toggle_expand_node(self.node.id)

    def _toggle_expand_parent(self, _id: str) -> None:
        parent = self._get_parent(_id)
        if not parent or not parent.id:
            return

        self._toggle_expand_node(parent.id)

    def toggle_expand_parent(self) -> None:
        if self.highlighted is None:
            return

        if not self.node.id:
            return

        self._toggle_expand_parent(self.node.id)
