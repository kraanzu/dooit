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

    def setup(self, value: str) -> None:
        self.set_value(value)


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


class Urgency(Item):
    _value = 1

    def increase(self) -> None:
        return self.set_value(self._value + 1)

    def decrease(self) -> None:
        return self.set_value(self._value - 1)

    def set_value(self, val: Any) -> None:
        val = int(val)
        self._value = val


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
