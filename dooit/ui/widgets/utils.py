from typing import Iterable
from .simple_input import SimpleInput


class Component:
    """
    Component class to maintain each row's data
    """

    def __init__(
        self,
        item,
        depth: int = 0,
        index: int = 0,
        expanded: bool = False,
    ) -> None:
        self.item = item
        self.expanded = expanded
        self.depth = depth
        self.index = index
        self.fields = {
            field: SimpleInput(
                value=getattr(item, field),
            )
            for field in item.fields
        }

    def refresh(self) -> None:
        for field in self.fields.keys():
            self.fields[field] = SimpleInput(
                value=getattr(
                    self.item,
                    field,
                )
            )

    def get_field_values(self) -> Iterable[SimpleInput]:
        return self.fields.values()

    def toggle_expand(self) -> None:
        self.expanded = not self.expanded

    def expand(self, expand: bool = True) -> None:
        self.expanded = expand


class VerticalView:
    """
    Vertical view to manage scrolling
    """

    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b

    def fix_view(self, current: int) -> None:
        if self.a < 0:
            self.shift(abs(self.a))

        if current <= self.a:
            self.shift(current - self.a)

        if self.b <= current:
            self.shift(current - self.b)

    def shift_upper(self, delta) -> None:
        self.a += delta

    def shift_lower(self, delta) -> None:
        self.b += delta

    def shift(self, delta: int) -> None:
        self.shift_lower(delta)
        self.shift_upper(delta)

    def height(self) -> int:
        return self.b - self.a

    def range(self) -> Iterable[int]:
        if self.a < 0:
            self.shift(abs(self.a))

        return range(self.a, self.b + 1)
