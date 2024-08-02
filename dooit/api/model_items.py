import re
from os import environ
from typing import Any, Tuple
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dooit.utils.date_parser import parse

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

    _value: Any = None

    def __init__(self, model: Any) -> None:
        self.model = model
        self.model_kind = model.__class__.__name__.lower()

    def get_value(self) -> str:
        return self._value

    def validate_value(self) -> bool:
        """
        Validate the value before assignment
        """

        raise NotImplementedError

    def set_value(self, val: str):
        """
        Set the value after validation
        """
        raise NotImplementedError

    def get_sortable(self) -> Any:
        """
        Returns a value for item for sorting
        """
        raise NotImplementedError

    def save(self) -> str:
        return self._value

    def setup(self, value: str) -> None:
        self.set_value(value)

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
            now = datetime.now()
            if due < now:
                return "OVERDUE"
        else:
            today = datetime.today().date()
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

    def set_value(self, val: Any) -> None:
        self.pending = val != "COMPLETED"
        self.update_others()

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
            self.set_value("COMPLETED")
        else:
            self.set_value("PENDING")

    def get_sortable(self) -> Any:
        if self.value == "OVERDUE":
            return 1
        elif self.value == "PENDING":
            return 2
        else:
            return 3


class Description(Item):
    _default = ""
    _value = _default

    def clean(self, s: str):
        for i, j in enumerate(s):
            if j not in "+%":  # left striping as this messes up with other attrs
                return s[i:]

        return s

    def set_value(self, val: str) -> None:
        val = self.clean(val)
        if val and val != self._default:
            self._value = val

    def to_txt(self) -> str:
        return self._value

    def from_txt(self, txt: str) -> None:
        value = ""

        index = 0
        for index, i in enumerate(txt.split()[3:]):
            if i[0] not in "+@%":
                break

        for j in txt.split()[3 + index :]:
            value = value + j + " "

        self._value = value.strip()

    def get_sortable(self) -> Any:
        return self._value


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

    def set_value(self, val: str) -> None:
        val = val.strip()

        if not val or val == "none":
            self._value = None

        res, ok = parse(val)
        current_year = str(datetime.now().year)

        if ok and res:
            if res < datetime.today() and current_year not in val:
                res = res + relativedelta(years=1)

            self._value = res

    def save(self) -> str:
        if not self._value:
            return super().save()

        return str(self._value.timestamp())

    def setup(self, value: str) -> None:
        if value:
            try:
                self._value = datetime.fromtimestamp(float(value))
            except ValueError:
                super().setup(value)

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
    _value = 1

    def increase(self) -> None:
        return self.set_value(self._value + 1)

    def decrease(self) -> None:
        return self.set_value(self._value - 1)

    def set_value(self, val: Any) -> None:
        val = int(val)
        # TODO: move this to validation
        # if val < 1:
        #     return Warn("Urgency cannot be decreased further!")
        # if val > 4:
        #     return Warn("Urgency cannot be increased further!")

        self._value = val

    def to_txt(self) -> str:
        return f"({self._value})"

    def from_txt(self, txt: str) -> None:
        self.set_value(txt.split()[1][1])

    def get_sortable(self) -> Any:
        return -self._value


class Recurrence(Item):
    _value = ""

    def set_value(self, val: str) -> None:
        if not val:
            self._value = ""

        split_duration(val.strip())

        # TODO: move this to validation
        # if not res:
        #     return Warn("Cannot parse! Please use format: [b]<number><m/h/d/w>[/b]")

        self._value = val

        if self.model.due == "none" and val:
            if val[-1] in "dw":
                self.model.edit("due", "today")
            else:
                self.model.edit("due", "now")

    def to_txt(self) -> str:
        if self._value:
            return f"%{self._value}"

        return ""

    def from_txt(self, txt: str) -> None:
        for i in txt.split():
            if i[0] == "%":
                self._value = i[1:]
                break

    def get_sortable(self) -> Any:
        if not self._value:
            return timedelta.max
        else:
            frequency, value = split_duration(self._value)
            return timedelta(**{DURATION_LEGEND[frequency] + "s": int(value)})


class Effort(Item):
    _value = 0

    @property
    def value(self):
        if self._value:
            return str(self._value)

        return ""

    def set_value(self, val: str) -> None:
        if not val:
            self._value = ""

        if not val.isnumeric():
            return

        val_int = int(val)
        if val_int >= 0:
            self._value = val_int

        # TODO: move this to validation

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
                self.set_value(i[1:])
