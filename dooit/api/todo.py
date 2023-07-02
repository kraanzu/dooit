from typing import Any, List, Optional, TypeVar
from .model import Model, Result
from .item_concrete_creator import ItemConcreteCreator


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
    fields = ["description", "due", "urgency", "effort", "tags", "status", "recurrence"]
    sortable_fields = [
        "description",
        "due",
        "urgency",
        "effort",
        "status",
        "recurrence",
    ]

    def __init__(self, parent: Optional[T] = None) -> None:
        super().__init__(parent)
        itemCreator = ItemConcreteCreator()
        self._status = itemCreator.create_status(self)
        self._description = itemCreator.create_description(self)
        self._urgency = itemCreator.create_urgency(self)
        self._effort = itemCreator.create_effort(self)
        self._tags = itemCreator.create_tags(self)
        self._recurrence = itemCreator.create_recurrence(self)
        self._due = itemCreator.create_due(self)
        self.todos: List[Todo] = []

    @property
    def path(self):
        parent_path = self.parent.path if self.parent else ""
        return self.description + "/" + parent_path

    @property
    def effort(self):
        return self._effort.value

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

    def add_todo(self, index: int = 0, inherit: bool = False):
        return self.add_child(TODO, index, inherit)

    def edit(self, key: str, value: str) -> Result:
        res = super().edit(key, value)
        self._status.update_others()
        return res

    def toggle_complete(self) -> bool:
        return self._status.toggle_done()

    def decrease_urgency(self) -> None:
        self._urgency.decrease()

    def increase_urgency(self) -> None:
        self._urgency.increase()

    def to_data(self) -> str:
        """
        Return todo.txt format of the todo
        """

        status = self._status.to_txt()
        urgency = self._urgency.to_txt()
        due = self._due.to_txt()
        effort = self._effort.to_txt()
        tags = self._tags.to_txt()
        recur = self._recurrence.to_txt()
        description = self._description.to_txt()

        arr = [status, urgency, due, effort, tags, recur, description]
        arr = [i for i in arr if i]
        return " ".join(arr)

    def fill_from_data(self, data: str) -> None:
        self._status.from_txt(data)
        self._urgency.from_txt(data)
        self._due.from_txt(data)
        self._description.from_txt(data)
        self._recurrence.from_txt(data)
        self._effort.from_txt(data)
        self._tags.from_txt(data)

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

    def _get_children(self, kind: str) -> List:
        """
        Get children list (todo)
        """
        if kind not in ["todo"]:
            raise TypeError(f"Cannot perform this operation for type {kind}")

        return self.todos
    
    def add_child(self, kind: str, index: int = 0, inherit: bool = False) -> Any:     
        """
        Adds a child to specified index (Defaults to first position)
        """
        if kind != "todo":
            raise TypeError(f"Cannot add child of kind {kind}")
        child = Todo(parent=self)
        if inherit and isinstance(self, Todo):
            child.fill_from_data(self.to_data())
            child._description.value = ""
            child._effort._value = 0
            child._tags.value = ""
            child.edit("status", "PENDING")

            children = self._get_children(kind)
            children.insert(index, child)

        return child

