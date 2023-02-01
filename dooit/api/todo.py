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
    fields = ["description", "due", "urgency", "tags", "status", "recurrence"]

    def __init__(self, parent: Optional[T] = None) -> None:
        from .model_items import Status, Due, Urgency, Recurrence, Tags, Description

        super().__init__(parent)
        self._status = Status(self)
        self._description = Description(self)
        self._urgency = Urgency(self)
        self._tags = Tags(self)
        self._recurrence = Recurrence(self)
        self._due = Due(self)
        self.todos: List[Todo] = []

    @property
    def path(self):
        parent_path = self.parent.path if self.parent else ""
        return self.description + "/" + parent_path

    @property
    def urgency(self):
        return self._urgency.value

    @property
    def description(self):
        return self._description.value

    @property
    def recurrence(self):
        return self._recurrence.value

    @property
    def due(self):
        return self._due.value

    @property
    def status(self):
        return self._status.value

    @property
    def tags(self):
        return self._tags.value

    def toggle_complete(self):
        return self._status.toggle_done()

    def decrease_urgency(self) -> None:
        self._urgency.decrease()

    def increase_urgency(self) -> None:
        self._urgency.increase()

    def to_data(self) -> str:
        """
        Return todo.txt format of the todo
        """

        tags = self._tags.to_txt()
        due = self._due.to_txt()
        recur = self._recurrence.to_txt()
        status = self._status.to_txt()
        urgency = self._urgency.to_txt()
        description = self._description.to_txt()

        arr = [status, urgency, due, tags, recur, description]
        arr = [i for i in arr if i]
        return " ".join(arr)

    def fill_from_data(self, data: str) -> None:
        self._status.from_txt(data)
        self._urgency.from_txt(data)
        self._due.from_txt(data)
        self._description.from_txt(data)
        self._recurrence.from_txt(data)

    def commit(self) -> List[Any]:
        if self.todos:
            return [
                self.to_data(),
                [child.commit() for child in self.todos],
            ]
        else:
            return [self.to_data()]

    def from_data(self, data: List) -> None:
        self.fill_from_data(data[0])
        if len(data) > 1:
            for i in data[1]:
                child_todo = self.add_child(kind="todo", index=len(self.todos))
                child_todo.from_data(i)
