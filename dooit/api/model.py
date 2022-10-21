from typing import Any, Dict, List, Optional, Type, Union

from ..utils.uuid import generate_uuid

MaybeModel = Union["Model", None]


class Model:
    """
    Model class to for the base tree structure
    """

    fields = []

    def __init__(
        self,
        parent: Optional["Model"] = None,
    ) -> None:
        from ..api.workspace import Workspace
        from ..api.todo import Todo

        self.todo_type: Type = None
        self.name = generate_uuid(self.__class__.__name__)
        self.parent = parent

        self.workspaces: List[Workspace] = []
        self.todos: List[Todo] = []

    def _get_children(self, kind: str) -> List:
        return self.workspaces if kind == "workspace" else self.todos

    def _get_child_index(self, kind: str, name: str) -> int:
        """
        Get child index by attr
        """

        for i, j in enumerate(self._get_children(kind)):
            if j.name == name:
                return i

        return -1

    def _get_index(self, kind: str) -> int:
        """
        Get items's index among it's siblings
        """

        if not self.parent:
            return -1

        return self.parent._get_child_index(kind, self.name)

    def edit(self, key: str, value: str):
        """
        Edit item's attrs
        """

        setattr(self, key, value)

    def shift_up(self, kind: str):
        """
        Shift the item one place up among its siblings
        """

        idx = self._get_index(kind)

        if idx in [0, -1]:
            return

        # NOTE: parent != None because -1 condition is checked
        arr = self.parent._get_children(kind)
        arr[idx], arr[idx - 1] = arr[idx - 1], arr[idx]

    def shift_down(self, kind: str):
        """
        Shift the item one place down among its siblings
        """

        idx = self._get_index(kind)

        if idx == -1:
            return

        # NOTE: parent != None because -1 condition is checked
        arr = self.parent._get_children(kind)
        if idx == len(arr) - 1:
            return

        arr[idx], arr[idx + 1] = arr[idx + 1], arr[idx]

    def prev_sibling(self, kind: str) -> MaybeModel:
        """
        Returns previous sibling item, if any, else None
        """

        if not self.parent:
            return

        idx = self.parent._get_child_index(kind, self.name)

        if idx:
            return self._get_children(kind)[idx - 1]

    def next_sibling(self, kind: str) -> MaybeModel:
        """
        Returns next sibling item, if any, else None
        """

        if not self.parent:
            return

        idx = self.parent._get_child_index(kind, self.name)
        arr = self.parent._get_children(kind)

        if idx < len(arr) - 1:
            return arr[idx + 1]

    def add_sibling(self, kind: str) -> "Model":
        """
        Add item sibling
        """

        if self.parent:
            idx = self.parent._get_child_index(kind, self.name)
            return self.parent.add_child(kind, idx + 1)
        else:
            return self.add_child(kind, 0)

    def add_child(self, kind: str, index: int = 0) -> "Model":
        """
        Adds a child to specified index (Defaults to first position)
        """
        from ..api.workspace import Workspace
        from ..api.todo import Todo

        child = Workspace(parent=self) if kind == "workspace" else Todo(parent=self)

        children = self._get_children(kind)
        children.insert(index, child)

        return child

    def remove_child(self, kind: str, name: str):
        """
        Remove the child based on attr
        """

        idx = self._get_child_index(kind, name)
        self._get_children(kind).pop(idx)

    def drop(self, kind: str):
        """
        Delete the item
        """

        if self.parent:
            self.parent.remove_child(kind, self.name)

    def sort(self, kind: str, attr: str):
        """
        Sort the children based on specific attr
        """

        if self.parent:
            children = self.parent._get_children(kind)
            children.sort(key=lambda x: getattr(x, attr))

    def commit(self):
        """
        Get a object summary that can be stored
        """

        return {
            getattr(
                child,
                "about",
            ): child.commit()
            for child in self.workspaces
        }

    def from_data(self, data: Dict[str, Any]):
        """
        Fill in the attrs from data provided
        """

        for i, j in data.items():
            self.add_child("workspace")
            self.workspaces[-1].edit("about", i)
            self.workspaces[-1].from_data(j)
