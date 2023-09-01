from datetime import datetime
from typing import Any, List, Optional, Union, Dict
from .model import Model, Result


TODO = "todo"
OPTS = {
    "PENDING": "x",
    "COMPLETED": "X",
    "OVERDUE": "O",
}


def reversed_dict(d):
    return {j: i for i, j in d.items()}


class Todo(Model):
    fields = ["description", "due", "urgency", "effort", "status", "recurrence"]

    sortable_fields = [
        "description",
        "due",
        "urgency",
        "effort",
        "status",
    ]

    def __init__(self, parent: Optional[Model] = None) -> None:
        from .model_items import (
            Status,
            Due,
            Urgency,
            Recurrence,
            Description,
            Effort,
        )

        super().__init__(parent)
        self._status = Status(self)
        self._description = Description(self)
        self._urgency = Urgency(self)
        self._effort = Effort(self)
        self._recurrence = Recurrence(self)
        self._due = Due(self)
        self.todos: List[Todo] = []

    @property
    def effort(self):
        return self._effort.value

    @property
    def urgency(self):
        return str(self._urgency.value)

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
    def tags(self) -> List[str]:
        return [i for i in self.description.split() if i[0] == "@"]

    def add_child(
        self, kind: str = "todo", index: int = 0, inherit: bool = False
    ) -> Any:
        if kind != "todo":
            raise TypeError(f"Cannot add child of kind {kind}")

        return super().add_child(kind, index, inherit)

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

    def to_data(self) -> Dict[str, str]:
        """
        Return storable form of todo
        """

        return {
            "uuid": self._uuid,
            "status": self._status.save(),
            "urgency": self._urgency.save(),
            "description": self._description.save(),
            "due": self._due.save(),
            "effort": self._effort.save(),
            "recurrence": self._recurrence.save(),
        }

    def fill_from_data(
        self, data: Union[Dict, str], overwrite_uuid: bool = True
    ) -> None:
        if isinstance(data, str):
            self.extract_data_old(data)
        else:
            self.extract_data_new(data, overwrite_uuid)

    # WARNING: This will be deprecated in future versions
    def extract_data_old(self, data: str):
        self._status.from_txt(data)
        self._urgency.from_txt(data)
        self._due.from_txt(data)
        self._description.from_txt(data)
        self._recurrence.from_txt(data)
        self._effort.from_txt(data)

    def extract_data_new(self, data: Dict[str, str], overwrite_uuid: bool = True):
        def get(key: str) -> str:
            return data.get(key, "")

        if overwrite_uuid:
            self._uuid = get("uuid")

        self._status.setup(get("status"))
        self._urgency.setup(get("urgency"))
        self._due.setup(get("due"))
        self._description.setup(get("description"))
        self._recurrence.setup(get("recurrence"))
        self._effort.setup(get("effort"))

    def commit(self) -> List[Any]:
        if self.todos:
            return [
                self.to_data(),
                [child.commit() for child in self.todos],
            ]
        else:
            return [self.to_data()]

    def from_data(self, data: List, overwrite_uuid: bool = True) -> None:
        self.fill_from_data(data[0], overwrite_uuid)
        if len(data) > 1:
            for i in data[1]:
                child_todo = self.add_child(kind="todo", index=len(self.todos))
                child_todo.from_data(i, overwrite_uuid)

    # ----------- HELPER FUNCTIONS --------------
    def has_due_date(self) -> bool:
        return bool(self._due._value)

    def is_due_today(self) -> bool:
        value = self._due._value
        return bool(value and (value.date() == datetime.today().date()))

    def is_completed(self) -> bool:
        return self.status == "COMPLETED"

    def is_pending(self) -> bool:
        return self.status == "PENDING"

    def is_overdue(self) -> bool:
        return self.status == "OVERDUE"
