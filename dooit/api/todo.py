import re
from typing import Any, List, Optional, Tuple, TypeVar
from .model import Model
from dateparser import parse
from datetime import datetime, timedelta


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
    fields = ["desc", "due", "urgency", "tags", "status", "recur", "eta"]

    def __init__(self, parent: Optional[T] = None) -> None:
        super().__init__(parent)

        self._desc = ""
        self.urgency = 4

        self._est = ""
        self._due = "none"
        self._done = False
        self._tags = ""
        self._recur = ""
        self.todos: List[Todo] = []

        self.duration_legend = {
            "m": "minute",
            "h": "hour",
            "d": "day",
            "w": "week",
        }

    def _split_duration(self, duration: str) -> Tuple[str, str]:
        return duration[-1], duration[:-1]

    def _is_valid(self, duration: str) -> bool:
        if not duration:
            return True

        sign, frequency = self._split_duration(duration)
        if sign not in self.duration_legend.keys() or not re.match(r"\d+", frequency):
            return False

        return True

    def _format_duration(self, duration: str):

        if not duration:
            return ""

        sign, frequency = self._split_duration(duration)
        name = self.duration_legend[sign]
        if int(frequency) > 1:
            name += "s"

        return f"{frequency} {name}"

    @property
    def desc(self):
        return self._desc

    def set_desc(self, val: str):
        if not val:
            return False
        else:
            self._desc = val
            return True

    @property
    def eta(self):
        return self._format_duration(self._est)

    def set_eta(self, val: str):
        if self._is_valid(val):
            self._est = val

    @property
    def recur(self):

        if not self._recur:
            return ""

        return f"Every {self._format_duration(self._recur)}"

    def set_recur(self, val: str):

        if not val:
            self._recur = ""
            return

        if self._is_valid(val):
            self._recur = val

    @property
    def due(self):
        return self._due

    def set_due(self, val: str):
        if val.lower() == "none":
            self._due = "none"

        res = parse(val)
        if res:
            self._due = res.strftime(r"%m-%d-%y")

    @property
    def status(self):
        if self._done:
            return "COMPLETED"
        else:
            return "PENDING"

    @property
    def tags(self):
        return self._tags

    def set_tags(self, val: str):
        self._tags = ", ".join([i.strip() for i in val.split(",")])

    def toggle_complete(self):
        self._done = not self._done
        if self._done and self._recur:
            due = datetime.strptime(self._due, "%m-%d-%y")
            sign, frequency = self._split_duration(self._recur)
            frequency = int(frequency)

            time_to_add = timedelta(
                **{
                    f"{self.duration_legend[sign]}s": frequency,
                }
            )

            self.set_due(datetime.strftime(due + time_to_add, "%m-%d-%y"))

    def decrease_urgency(self) -> None:
        self.urgency = max(self.urgency - 1, 1)

    def increase_urgency(self) -> None:
        self.urgency = min(self.urgency + 1, 4)

    def to_data(self) -> str:
        """
        Return todo.txt format of the todo
        """

        return f"{OPTS[self.status]} ({self.urgency}) due:{self._due or 'None'} {self._desc}"

    def fill_from_data(self, data: str) -> None:
        status, urgency, due, *desc = data.split()

        status = True if status == "x" else False
        desc = " ".join(desc)

        due = due[4:]
        if due == "None":
            due = ""

        urgency = int(urgency[1:-1])

        self._desc = desc
        self.urgency = urgency
        self._due = due
        self._done = status

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
