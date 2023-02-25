import re
from os import environ
from typing import Any, Tuple
from datetime import datetime, timedelta
from dooit.utils.dateparser import parse
from .model import Result, Ok, Warn, Err

DATE_ORDER = environ.get("DOOIT_DATE_ORDER", "DMY")
DATE_FORMAT = (
    "-".join(list(DATE_ORDER)).replace("D", "%d").replace("M", "%m").replace("Y", "%y")
)
TIME_FORMAT = "@%H:%M"
DURATION_LEGEND = {
    "m": "minute",
    "h": "hour",
    "d": "day",
    "w": "week",
}
OPTS = {
    "PENDING": "x",
    "COMPLETED": "X",
    "OVERDUE": "O",
}
CASUAL_FORMAT = "%d %h @ %H:%M"


def split_duration(duration: str) -> Tuple[str, str]:
    if re.match(r"^(\d+)[mhdw]$", duration):
        return duration[-1], duration[:-1]
    else:
        return tuple()


class Item:
    """
    A workspace/todo item/param
    """

    value: Any

    def __init__(self, model: Any) -> None:
        self.model = model
        self.model_kind = model.__class__.__name__.lower()

    def set(self, val: str) -> Result:
        """
        Set the value after validation
        """
        raise NotImplementedError

    def get_sortable(self) -> Any:
        """
        Returns a value for item for sorting
        """
        raise NotImplementedError

    def to_txt(self) -> str:
        """
        Convert to storable format
        """
        raise NotImplementedError

    def from_txt(self, txt: str) -> None:
        """
        Parse from stored todo string
        """
        raise NotImplementedError


class Status(Item):
    pending = True

    @property
    def value(self):
        self.handle_recurrence()

        if not self.pending:
            return "COMPLETED"

        due = self.model._due._value
        if not due or due == "none":  # why? dateparser slowpok
            return "PENDING"

        if due.hour or due.minute:
            now = parse("now")
            if due < now:
                return "OVERDUE"
        else:
            today = parse("today").date()
            due = due.date()
            if today > due:
                return "OVERDUE"

        return "PENDING"

    def toggle_done(self) -> bool:
        self.pending = not self.pending
        self.update_others()
        return not self.pending

    def handle_recurrence(self):
        if not self.model.recurrence:
            return

        if self.pending:
            return

        due = self.model._due._value
        if not due or due == "none":
            return

        sign, frequency = split_duration(self.model._recurrence.value)
        frequency = int(frequency)
        time_to_add = timedelta(**{f"{DURATION_LEGEND[sign]}s": frequency})
        new_time = due + time_to_add

        if new_time >= datetime.now():
            return

        self.model.edit("due", new_time.strftime(DATE_FORMAT))
        self.pending = True

    def set(self, val: Any) -> Result:
        self.pending = val != "COMPLETED"
        self.update_others()
        return Ok()

    def update_others(self):

        # Update ancestors
        current = self.model
        while parent := current.parent:
            if hasattr(parent, "status"):
                if parent.todos:
                    is_done = all(i.status == "COMPLETED" for i in parent.todos)
                    parent._status.pending = not is_done
                current = parent
            else:
                break

        # Update children
        def update_children(todo=self.model, status=self.pending):

            todo._status.pending = status
            for i in todo.todos:
                update_children(i, status)

        update_children()

    def to_txt(self) -> str:
        return "X" if self.value == "COMPLETED" else "O"

    def from_txt(self, txt: str) -> None:
        status = txt.split()[0]
        if status == "X":
            self.set("COMPLETED")
        else:
            self.set("PENDING")

    def get_sortable(self) -> Any:
        if self.value == "OVERDUE":
            return 1
        elif self.value == "PENDING":
            return 2
        else:
            return 3


class Description(Item):
    value = ""

    def clean(self, s: str):
        for i, j in enumerate(s):
            if j not in "@+%":  # left striping as this messes up with other attrs
                return s[i:]

        return s

    def set(self, value: Any) -> Result:
        value = self.clean(value)
        if value:
            new_index = -1
            if self.model:
                new_index = self.model.parent._get_child_index(
                    self.model_kind, description=value
                )

            old_index = self.model._get_index(self.model_kind)

            if new_index != -1 and new_index != old_index:
                return Err(
                    f"A {self.model_kind} with same description is already present"
                )
            else:
                self.value = value
                return Ok()

        return Err("Can't leave description empty!")

    def to_txt(self) -> str:
        return self.value

    def from_txt(self, txt: str) -> None:
        value = ""
        for i in txt.split()[3:]:
            if i[0].isalpha():
                value = value + i + " "

        self.value = value.strip()

    def get_sortable(self) -> Any:
        return self.value


class Due(Item):
    _value = None

    @property
    def value(self):
        if not self._value:
            return "none"

        time = self._value.time()
        if time.hour == time.minute == 0:
            return self._value.strftime("%d %h")
        else:
            return self._value.strftime("%d %h %H:%M")

    def set(self, val: str) -> Result:
        val = val.strip()

        if not val or val == "none":
            self._value = None
            return Ok("Due removed for the todo")

        if val.strip() == "today":
            val = "today 0:0"  # remove un-necessary time

        res = parse(val)
        if res:
            self._value = res
            return Ok(f"Due date changed to [b cyan]{self.value}[/b cyan]")

        return Warn("Cannot parse the string!")

    def to_txt(self) -> str:
        if self._value:
            t = self._value.time()
            if t.hour == t.minute == 0:
                save = self._value.strftime(DATE_FORMAT)
            else:
                save = self._value.strftime(DATE_FORMAT + TIME_FORMAT)
        else:
            save = "none"
        return f"due:{save}"

    def from_txt(self, txt: str) -> None:
        value = txt.split()[2].lstrip("due:").lower()
        if value != "none":
            if "@" in value:
                self._value = datetime.strptime(value, DATE_FORMAT + TIME_FORMAT)
            else:
                self._value = datetime.strptime(value, DATE_FORMAT)

    def get_sortable(self) -> Any:
        return self._value or datetime.max


class Urgency(Item):
    value = 1

    def increase(self) -> Result:
        return self.set(self.value + 1)

    def decrease(self) -> Result:
        return self.set(self.value - 1)

    def set(self, val: Any) -> Result:

        val = int(val)
        if val < 1:
            return Warn("Urgency cannot be decreased further!")
        if val > 4:
            return Warn("Urgency cannot be increased further!")

        self.value = val
        return Ok()

    def to_txt(self) -> str:
        return f"({self.value})"

    def from_txt(self, txt: str) -> None:
        self.set(txt.split()[1][1])

    def get_sortable(self) -> Any:
        return -self.value


class Tags(Item):
    value = ""

    def set(self, val: str) -> Result:
        tags = [i.strip() for i in val.split(",") if i]
        self.value = ",".join(set(tags))
        return Ok()

    def add_tag(self, tag: str):
        return self.set(self.value + "," + tag)

    def to_txt(self):
        return " ".join(f"@{i}" for i in self.value.split(",") if i)

    def from_txt(self, txt: str) -> None:
        flag = True
        for i in txt.split()[3:]:
            if i[0] == "@":
                self.add_tag(i[1:])
                flag = False
            else:
                if not flag:
                    break


class Recurrence(Item):
    value = ""

    def set(self, val: str) -> Result:
        if not val:
            self.value = ""
            return Ok("Recurrence removed")

        res = split_duration(val.strip())
        if not res:
            return Warn("Cannot parse! Please use format: [b]<number><m/h/d/w>[/b]")

        self.value = val
        if self.model.due == "none":
            if val[-1] in "dw":
                self.model.edit("due", "today")
            else:
                self.model.edit("due", "now")

            return Ok(f"Recurrence set for {self.value} [i]starting today[/i]")

        return Ok(f"Recurrence set for {self.value}")

    def to_txt(self) -> str:
        if self.value:
            return f"%{self.value}"

        return ""

    def from_txt(self, txt: str) -> None:
        for i in txt.split():
            if i[0] == "%":
                self.value = i[1:]
                break

    def get_sortable(self) -> Any:
        if not self.value:
            return timedelta.max
        else:
            frequency, value = split_duration(self.value)
            return timedelta(**{DURATION_LEGEND[frequency] + "s": int(value)})


class Effort(Item):
    _value = 0

    @property
    def value(self):
        if self._value:
            return str(self._value)

        return ""

    def set(self, val: str) -> Result:
        if not val:
            self._value = ""
            return Ok("Effort removed for the todo")

        if not val.isnumeric():
            return Warn("Only numeric values allowed")

        val_int = int(val)
        if val_int >= 0:
            self._value = val_int
            return Ok()

        return Warn("Cannot decrease effort below zero")

    def get_sortable(self) -> Any:
        if self._value:
            return self._value
        else:
            # NOTE: If someone opens an issue for this...
            # my ans: if its above 100 then probably the other tasks require low effort
            return 10**2

    def to_txt(self) -> str:
        if self.value:
            return f"+{self.value}"
        else:
            return ""

    def from_txt(self, txt: str) -> None:
        for i in txt.split()[3:]:
            if i[0] == "+":
                self.set(i[1:])
