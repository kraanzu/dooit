from typing import List, Optional, Type, Union

MaybeModel = Union["Model", None]


class Model:
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

        for i, j in enumerate(self.children):
            if j.name == name:
                return i

        return -1

    def _get_child(self, name) -> "Model":
        return self.children[name]

    def _get_index(self) -> int:
        if not self.parent:
            return -1

        return self.parent._get_child_index(self.name)

    def edit(self, key: str, value: str):
        setattr(self, key, value)

    def shift_up(self):

        idx = self._get_index()

        if idx in [0, -1]:
            return

        # NOTE: parent != None because -1 condition is checked
        arr = self.parent.children
        arr[idx], arr[idx - 1] = arr[idx - 1], arr[idx]

    def shift_down(self):

        idx = self._get_index()

        if idx == -1:
            return

        # NOTE: parent != None because -1 condition is checked
        arr = self.parent.children
        if idx == len(arr) - 1:
            return

        arr[idx], arr[idx + 1] = arr[idx + 1], arr[idx]

    def prev_sibling(self) -> MaybeModel:
        if not self.parent:
            return

        idx = self.parent._get_child_index(self.name)

        if idx:
            return self.parent.children[idx - 1]

    def next_sibling(self) -> MaybeModel:
        if not self.parent:
            return

        idx = self.parent._get_child_index(self.name)
        total = len(self.parent.children)

        if idx != total - 1:
            return self.parent.children[idx + 1]

    def add_sibling(self):
        if self.parent:
            idx = self.parent._get_child_index(self.name)
            self.parent.add_child(idx + 1)

    def add_child(self, index: Optional[int] = None):

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
        idx = self._get_child_index(name)
        self.children.pop(idx)

    def drop(self):
        if self.parent:
            self.parent.remove_child(self.name)

    def sort_children(self, field: str):
        self.children.sort(key=lambda x: getattr(x, field))

    def commit(self):
        return {getattr(child, "about"): child.commit() for child in self.children}

    def from_data(self, data):

        for i, j in data.items():
            self.add_child()
            self.children[-1].edit("about", i)
            self.children[-1].from_data(j)
