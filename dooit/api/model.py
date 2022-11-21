from typing import Any, Dict, List, Optional, TypeVar
from uuid import uuid4
from dataclasses import dataclass
from .storage import Storage

T = TypeVar("T", bound="Model")
MaybeModel = Optional["Model"]


def colored(text: str, color: str):
    return f"[{color}]{text}[/{color}]"

@dataclass
class Response:
    ok: bool
    message: Optional[str] = None
    hint: Optional[str] = None

    def text(self):
        text = ""

        if self.message:
            text += " "
            text += colored(self.message, "green" if self.ok else "red")

        if self.hint:
            text += " "
            text += colored(self.hint, "yellow")

        return text


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

        self.name = str(uuid4())
        self.parent = parent

        self.workspaces: List[Workspace] = []
        self.todos: List[Todo] = []

    @property
    def path(self):
        return "$"

    def _get_children(self, kind: str) -> List:
        return self.workspaces if kind == "workspace" else self.todos

    def _get_child_index(self, kind: str, **kwargs) -> int:
        """
        Get child index by attr
        """

        key, value = list(kwargs.items())[0]
        for i, j in enumerate(self._get_children(kind)):
            if getattr(j, key) == value:
                return i

        return -1

    def _get_index(self, kind: str) -> int:
        """
        Get items's index among it's siblings
        """

        if not self.parent:
            return -1

        return self.parent._get_child_index(kind, name=self.name)

    def edit(self, key: str, value: str) -> Response:
        """
        Edit item's attrs
        """

        func = f"set_{key}"
        if hasattr(self, func):
            return getattr(self, func)(value)
        else:
            return Response(False, "Invalid Request!")

    def shift_up(self, kind: str) -> None:
        """
        Shift the item one place up among its siblings
        """

        idx = self._get_index(kind)

        if idx in [0, -1]:
            return

        if not self.parent:
            return
        arr = self.parent._get_children(kind)
        arr[idx], arr[idx - 1] = arr[idx - 1], arr[idx]

    def shift_down(self, kind: str) -> None:
        """
        Shift the item one place down among its siblings
        """

        idx = self._get_index(kind)

        if idx == -1 or not self.parent:
            return

        arr = self.parent._get_children(kind)
        if idx == len(arr) - 1:
            return

        arr[idx], arr[idx + 1] = arr[idx + 1], arr[idx]

    def prev_sibling(self: T, kind: str) -> Optional[T]:
        """
        Returns previous sibling item, if any, else None
        """

        if not self.parent:
            return

        idx = self.parent._get_child_index(kind, name=self.name)

        if idx:
            return self._get_children(kind)[idx - 1]

    def next_sibling(self: T, kind: str) -> Optional[T]:
        """
        Returns next sibling item, if any, else None
        """

        if not self.parent:
            return

        idx = self.parent._get_child_index(kind, name=self.name)
        arr = self.parent._get_children(kind)

        if idx < len(arr) - 1:
            return arr[idx + 1]

    def add_sibling(self: T, kind: str) -> T:
        """
        Add item sibling
        """

        if self.parent:
            idx = self.parent._get_child_index(kind, name=self.name)
            return self.parent.add_child(kind, idx + 1)
        else:
            return self.add_child(kind, 0)

    def add_child(self, kind: str, index: int = 0) -> Any:
        """
        Adds a child to specified index (Defaults to first position)
        """
        from ..api.workspace import Workspace
        from ..api.todo import Todo

        child = (
            Workspace(
                parent=self,
            )
            if kind == "workspace"
            else Todo(
                parent=self,
            )
        )

        children = self._get_children(kind)
        children.insert(index, child)

        return child

    def insert_item(self, item, insert_as_child=False) -> None:
        """
        Insert item at current location and clear clipboard each time we paste
        """
        from ..api.workspace import Workspace
        kind = "workspace" if isinstance(item, Workspace) else "todo"
        if item != None and self.parent:
            if insert_as_child: 
                idx = self._get_child_index(kind, name=self.name)
                children = self._get_children(kind)
                item.parent = self
                children.insert(idx + 1, item)
            else:
                idx = self.parent._get_child_index(kind, name=self.name)
                item.parent = self.parent
                children = self.parent._get_children(kind)
                children.insert(idx + 1, item)
            Storage.clipboard = None

    def remove_child(self, kind: str, name: str) -> Any:
        """
        Remove the child based on attr
        """

        idx = self._get_child_index(kind, name=name)
        if self.parent:
            Storage.clipboard = self._get_children(kind).pop(idx)
            return Storage.clipboard

    def drop(self, kind: str) -> None:
        """
        Delete the item
        """

        if self.parent:
            self.parent.remove_child(kind, self.name)

    def sort(self, kind: str, attr: str) -> None:
        """
        Sort the children based on specific attr
        """

        if self.parent:
            children = self.parent._get_children(kind)
            children.sort(key=lambda x: getattr(x, attr))

    def commit(self) -> Dict[str, Any]:
        """
        Get a object summary that can be stored
        """

        return {
            getattr(
                child,
                "desc",
            ): child.commit()
            for child in self.workspaces
        }

    def from_data(self, data: Dict[str, Any]) -> None:
        """
        Fill in the attrs from data provided
        """

        for i, j in data.items():
            self.add_child("workspace")
            self.workspaces[-1].edit("desc", i)
            self.workspaces[-1].from_data(j)
