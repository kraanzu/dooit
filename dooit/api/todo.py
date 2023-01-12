import re
from typing import Any, List, Optional, Tuple, TypeVar
from dateparser import parse
from datetime import date, datetime, timedelta
from .model import Model, Response


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

        from dooit.utils.conf_reader import Config

        self.DATE_ORDER = Config().get("DATE_ORDER")

        self._desc = ""
        self.urgency = 4

        self._eta = ""
        self._due = "none"
        self._done = False
        self._overdue = False
        self._tags = []
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

        if not re.match(r"^(\d+)[mhdw]$", duration):
            return False

        return True

    def _format_duration(self, duration: str):

        if not duration or not self._is_valid(duration):
            return ""

        sign, frequency = self._split_duration(duration)
        name = self.duration_legend[sign]
        if int(frequency) > 1:
            name += "s"

        return f"{frequency} {name}"

    @property
    def path(self):
        parent_path = self.parent.path if self.parent else ""
        return self.desc + "/" + parent_path

    @property
    def desc(self):
        return self._desc

    def set_desc(self, value: str) -> Response:
        if value:
            new_index = -1
            if self.parent:
                new_index = self.parent._get_child_index("todo", desc=value)

            old_index = self._get_index("todo")

            if new_index != -1 and new_index != old_index:
                return Response(
                    False,
                    "A todo with same description is already present",
                )
            else:
                self._desc = value
                return Response(True)

        return Response(
            False,
            "Can't leave description empty!",
        )

    @property
    def eta(self):
        return self._format_duration(self._eta)

    def set_eta(self, val: str) -> Response:
        if not self._is_valid(val):
            return Response(False, "Invalid Format!")

        self._eta = val
        return Response(True)

    @property
    def recur(self):

        if not self._recur:
            return ""

        return f"Every {self._format_duration(self._recur)}"

    def set_recur(self, val: str):

        if not val:
            self._recur = ""
            return Response(True, "Recurrence removed for the todo")

        if self._is_valid(val):
            self._recur = val
            return Response(True)

        return Response(False, "Invalid Format!")

    @property
    def due(self):
        return self._due

    def set_due(self, val: str) -> Response:

        if val == "":
            self._due = ""
            return Response(True, "Due removed for the todo")

        res = parse(val, settings={"DATE_ORDER": self.DATE_ORDER})
        if res:
            try:
                format = "-".join(list(self.DATE_ORDER))
                for old, new in [["D", "%d"], ["M", "%m"], ["Y", "%y"]]:
                    format = format.replace(old, new)

                self._overdue = datetime.now() > res
                self._due = res.strftime(format)
                return Response(
                    True, f"Due date changed to [b cyan]{self.due}[/b cyan]"
                )
            except:
                return Response(
                    False,
                    "Invalid Format!",
                )

        return Response(False, "Cannot parse the string!")

    @property
    def status(self):
        if self._done:
            return "COMPLETED"
        else:
            if self._overdue:
                return "OVERDUE"

            return "PENDING"

    @property
    def tags(self):
        return ", ".join(self._tags)

    def set_tags(self, val: str) -> Response:
        self._tags = [i.strip() for i in val.split(",")]
        return Response(True)

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

        tags = " ".join([f"@{i}" for i in self._tags])
        due = "due:" + (self._due or "None")
        recur = f"%{self._recur}" if self._recur else ""
        eta = f"+{self._eta}" if self._eta else ""
        status = OPTS[self.status]
        urgency = f"({self.urgency})"
        desc = self._desc

        arr = [status, urgency, due, tags, recur, eta, desc]
        arr = [i for i in arr if i]
        return " ".join(arr)

    def fill_from_data(self, data: str) -> None:
        status, urgency, due, *arr = data.split()
        brr = []

        for i in arr:
            if i.startswith("@"):  # tags
                self._tags.append(i[1:])
            elif i.startswith("+"):  # eta
                self._eta = i[1:]
            elif i.startswith("%"):  # recurrence
                self._recur = i[1:]
            else:
                brr.append(i)

        status = True if status == "X" else False
        desc = " ".join(brr)

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

    def add_todo(self: T, index: int = 0) -> T:
        return super().add_child(TODO, index)

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
                child_todo: Todo = self.add_todo(index=len(self.todos))
                child_todo.from_data(i)
