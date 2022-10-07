from typing import Any, Dict, List, Optional, Type, Union

MaybeModel = Union["Model", None]


class Model:
    """
    Model class to for the base tree structure
    """

    _ctype_counter: int = 1
    nomenclature: str = "None"
    fields = []

    def __init__(
        self,
        name: str,
        parent: Optional["Model"] = None,
    ) -> None:
        self.ctype: Type = type(self)
        self.name = name
        self.parent = parent
        self.children: List = []

    def _get_child_index(self, name: str) -> int:
        """
        Get child index by attr
        """

        for i, j in enumerate(self.children):
            if j.name == name:
                return i

        return -1

    def _get_index(self) -> int:
        """
        Get items's index among it's siblings
        """

        if not self.parent:
            return -1

        return self.parent._get_child_index(self.name)

    def edit(self, key: str, value: str):
        """
        Edit item's attrs
        """

        setattr(self, key, value)

    def shift_up(self):
        """
        Shift the item one place up among its siblings
        """

        idx = self._get_index()

        if idx in [0, -1]:
            return

        # NOTE: parent != None because -1 condition is checked
        arr = self.parent.children
        arr[idx], arr[idx - 1] = arr[idx - 1], arr[idx]

    def shift_down(self):
        """
        Shift the item one place down among its siblings
        """

        idx = self._get_index()

        if idx == -1:
            return

        # NOTE: parent != None because -1 condition is checked
        arr = self.parent.children
        if idx == len(arr) - 1:
            return

        arr[idx], arr[idx + 1] = arr[idx + 1], arr[idx]

    def prev_sibling(self) -> MaybeModel:
        """
        Returns previous sibling item, if any, else None
        """

        if not self.parent:
            return

        idx = self.parent._get_child_index(self.name)

        if idx:
            return self.parent.children[idx - 1]

    def next_sibling(self) -> MaybeModel:
        """
        Returns next sibling item, if any, else None
        """

        if not self.parent:
            return

        idx = self.parent._get_child_index(self.name)
        total = len(self.parent.children)

        if idx != total - 1:
            return self.parent.children[idx + 1]

    def add_sibling(self):
        """
        Add item sibling
        """

        if self.parent:
            idx = self.parent._get_child_index(self.name)
            self.parent.add_child(idx + 1)

    def add_child(self, index: Optional[int] = None):
        """
        Adds a child to specified index (Defaults to first position)
        """

        self._ctype_counter += 1
        child = self.ctype(
            name=f"{self.name}/{self.nomenclature}#{self._ctype_counter}".lstrip(
                "Manager/"
            ),
            parent=self,
        )

        if index:
            self.children.insert(index, child)
        else:
            self.children.insert(0, child)

    def remove_child(self, name: str):
        """
        Remove the child based on attr
        """

        idx = self._get_child_index(name)
        self.children.pop(idx)

    def drop(self):
        """
        Delete the item
        """

        if self.parent:
            self.parent.remove_child(self.name)

    def sort_children(self, attr: str):
        """
        Sort the children based on specific attr
        """

        self.children.sort(key=lambda x: getattr(x, attr))

    def commit(self):
        """
        Get a object summary that can be stored
        """

        return {getattr(child, "about"): child.commit() for child in self.children}

    def from_data(self, data: Dict[str, Any]):
        """
        Fill in the attrs from data provided
        """

        for i, j in data.items():
            self.add_child()
            self.children[-1].edit("about", i)
            self.children[-1].from_data(j)
