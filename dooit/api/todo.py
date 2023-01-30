import re
from typing import Any, List, Optional, Tuple, TypeVar
from dateparser import parse
from datetime import datetime, timedelta
from .model import Model, Result, Ok, Err, Warn


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
    fields = ["description", "due", "urgency", "tags", "status", "recurrence", "eta"]

    def __init__(self, parent: Optional[T] = None) -> None:
        super().__init__(parent)

        self._description = ""
        self.urgency = 4

        self._eta = ""
        self._due = "none"
        self._done = False
        self._overdue = False
        self._tags = []
        self._recurrence = ""
        self.todos: List[Todo] = []

        self.duration_legend = {
            "m": "minute",
            "h": "hour",
            "d": "day",
            "w": "week",
        }
        self.setup_date_formats()

    def setup_date_formats(self):
        from dooit.utils.conf_reader import Config

        self.DATE_ORDER = Config().get("DATE_ORDER")
        format = "-".join(list(self.DATE_ORDER))
        for old, new in [["D", "%d"], ["M", "%m"], ["Y", "%y"]]:
            format = format.replace(old, new)
        self.date_format = format

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
        return self.description + "/" + parent_path

    @property
    def description(self):
        return self._description

    def set_description(self, value: str) -> Result:
        if value:
            new_index = -1
            if self.parent:
                new_index = self.parent._get_child_index("todo", description=value)

            old_index = self._get_index("todo")

            if new_index != -1 and new_index != old_index:
                return Err(
                    "A todo with same description is already present",
                )
            else:
                self._description = value
                return Ok()

        return Err(
            "Can't leave description empty!",
        )

    @property
    def eta(self):
        return self._format_duration(self._eta)

    def set_eta(self, val: str) -> Result:
        if not self._is_valid(val):
            return Warn("Invalid Format! Use: <number><m/h/d/w>")

        self._eta = val
        return Ok()

    @property
    def recurrence(self):

        if not self._recurrence:
            return ""

        return f"Every {self._format_duration(self._recurrence)}"

    def set_recurrence(self, val: str):

        if flag := self.due == "none":
            self.set_due("now")

        if not val:
            self._recurrence = ""
            return Ok("Recurrence removed for the todo")

        if self._is_valid(val):
            self._recurrence = val
            if flag:
                return Ok(f"Recurrence set for {self.recurrence} starting today")
            else:
                return Ok(f"Recurrence set for {self.recurrence}")

        return Warn("Invalid Format! Use: <number><m/h/d/w>")

    @property
    def due(self):
        return self._due

    def set_due(self, val: str) -> Result:
        val = val.strip()

        if not val or val == "none":
            self._due = "none"
            return Ok("Due removed for the todo")

        res = parse(val, settings={"DATE_ORDER": self.DATE_ORDER})
        if res:
            self._overdue = datetime.now() > res
            self._due = res.strftime(self.date_format)
            return Ok(f"Due date changed to [b cyan]{self.due}[/b cyan]")

        return Warn("Cannot parse the string!")

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

    def set_tags(self, val: str) -> Result:
        self._tags = [i.strip() for i in val.split(",")]
        return Ok()

    def toggle_complete(self):
        self._done = not self._done
        if self._done and self._recurrence and self._due != "none":
            self._done = False
            due = datetime.strptime(self._due, self.date_format)
            sign, frequency = self._split_duration(self._recurrence)
            frequency = int(frequency)

            time_to_add = timedelta(
                **{
                    f"{self.duration_legend[sign]}s": frequency,
                }
            )

            self.set_due(datetime.strftime(due + time_to_add, self.date_format))

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
        recur = f"%{self._recurrence}" if self._recurrence else ""
        eta = f"+{self._eta}" if self._eta else ""
        status = OPTS[self.status]
        urgency = f"({self.urgency})"
        description = self._description

        arr = [status, urgency, due, tags, recur, eta, description]
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
                self._recurrence = i[1:]
            else:
                brr.append(i)

        status = True if status == "X" else False
        description = " ".join(brr)

        due = due[4:]
        if due == "None":
            due = ""

        urgency = int(urgency[1:-1])

        self.urgency = urgency
        self._done = status

        self.set_description(description)
        self.set_due(due)

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

    def from_data(self, data: List) -> None:
        self.fill_from_data(data[0])
        if len(data) > 1:
            for i in data[1]:
                child_todo = self.add_child(kind="todo", index=len(self.todos))
                child_todo.from_data(i)
