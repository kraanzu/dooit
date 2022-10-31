from typing import Any, List, Optional, TypeVar
from .model import Model


TODO = "todo"
OPTS = {
    "PENDING": "x",
    "COMPLETED": "X",
    "OVERDUE": "O",
}
T = TypeVar("T", bound="Model")


def reversed_dict(d):
    return {j: i for i, j in d.items()}


class Todo(Model):
    fields = ["desc", "due", "urgency", "tags"]

    def __init__(self, parent: Optional[T] = None) -> None:
        super().__init__(parent)

        self.desc = ""
        self.due = "today"
        self.urgency = 4
        self.status = "PENDING"
        self._tags = ""

        self.todos: List[Todo] = []

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, val: str):
        self._tags = ", ".join([i.strip() for i in val.split(",")])

    def decrease_urgency(self) -> None:
        self.urgency = max(self.urgency - 1, 0)

    def increase_urgency(self) -> None:
        self.urgency = min(self.urgency + 1, 4)

    def to_data(self) -> str:
        """
        Return todo.txt format of the todo
        """

        return (
            f"{OPTS[self.status]} ({self.urgency}) due:{self.due or 'None'} {self.desc}"
        )

    def fill_from_data(self, data: str) -> None:
        status, urgency, due, *desc = data.split()

        status = reversed_dict(OPTS)[status]
        desc = " ".join(desc)

        due = due[4:]
        if due == "None":
            due = ""

        urgency = int(urgency[1:-1])

        self.desc = desc
        self.urgency = urgency
        self.due = due
        self.status = status

    def commit(self) -> List[Any]:
        if self.todos:
            return [
                self.to_data(),
                [child.commit() for child in self.todos],
            ]
        else:
            return [
                self.to_data(),
            ]

    def add_child(self: T) -> T:
        return super().add_child(TODO)

    def add_sibling(self: T) -> T:
        return super().add_sibling(TODO)

    def shift_up(self) -> None:
        return super().shift_up(TODO)

    def shift_down(self) -> None:
        return super().shift_down(TODO)

    def next_sibling(self: T) -> Optional[T]:
        return super().next_sibling(TODO)

    def prev_sibling(self: T) -> Optional[T]:
        return super().prev_sibling(TODO)

    def drop(self) -> None:
        return super().drop(TODO)

    def sort(self, attr: str) -> None:
        return super().sort(TODO, attr)

    def from_data(self, data: List) -> None:
        self.fill_from_data(data[0])
        if len(data) > 1:
            for i in data[1]:
                child_todo: Todo = self.add_child()
                child_todo.from_data(i)
