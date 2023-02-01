import re
from typing import Any, Tuple
import dateparser
from datetime import datetime, timedelta
from dooit.utils.conf_reader import Config
from .model import Result, Ok, Warn, Err

DATE_ORDER = Config().get("DATE_ORDER")
DATE_FORMAT = (
    "-".join(list(DATE_ORDER)).replace("D", "%d").replace("M", "%m").replace("Y", "%y")
)
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
OPTS2 = {j: i for i, j in OPTS.items()}


def parse(date: str):
    return dateparser.parse(date, settings={"DATE_ORDER": DATE_ORDER})


def split_duration(duration: str) -> Tuple[str, str]:
    if re.match(r"^(\d+)[mhdw]$", duration):
        return duration[-1], duration[:-1]
    else:
        return tuple()


def format_duration(duration: str):

    res = split_duration(duration)
    if not res:
        return ""

    sign, frequency = res
    name = DURATION_LEGEND[sign]
    if int(frequency) > 1:
        name += "s"

    return f"{frequency} {name}"


class Item:
    value: Any

    def __init__(self, model: Any) -> None:
        self.model = model
        self.model_kind = model.__class__.__name__.lower()

    def set(self, val: Any) -> Result:
        raise NotImplementedError

    def get_sortable(self) -> Any:
        raise NotImplementedError

    def to_txt(self) -> str:
        raise NotImplementedError

    def from_txt(self, txt: str) -> None:
        raise NotImplementedError


class Status(Item):
    value = "PENDING"

    def toggle_done(self):
        if self.value != "COMPLETED":
            self.set("COMPLETED")
        else:
            self.set("PENDING")

    def set(self, val: Any) -> Result:
        if val == "COMPLETED":
            if self.model.recurrence:
                due = datetime.strptime(self.model.due, DATE_FORMAT)
                sign, frequency = split_duration(self.model._recurrence.value)
                frequency = int(frequency)

                time_to_add = timedelta(**{f"{DURATION_LEGEND[sign]}s": frequency})
                self.model.edit(
                    "due", datetime.strftime(due + time_to_add, DATE_FORMAT)
                )
                self.set("PENDING")
            else:
                self.value = "COMPLETED"
        else:
            due = self.model.due
            if due == "none":
                self.value = "PENDING"
            else:
                res = parse(due)
                now = parse("now")
                if res and now and res <= now:
                    self.value = "OVERDUE"
                else:
                    self.value = "PENDING"

        return Ok()

    def to_txt(self) -> str:
        return OPTS[self.get()]

    def from_txt(self, txt: str) -> None:
        status = txt.split()[0]
        if status == "X":
            self.set("COMPLETED")
        else:
            self.set("PENDING")


class Description(Item):
    value = ""

    def set(self, value: Any) -> Result:
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


class Due(Item):
    value = "none"

    def set(self, val: str) -> Result:
        val = val.strip()

        if not val or val == "none":
            self.value = "none"
            return Ok("Due removed for the todo")

        res = parse(val)
        if res:
            self.model._overdue = datetime.now() > res
            self.value = res.strftime(DATE_FORMAT)
            if self.model.status != "COMPLETED":
                self.model.edit("status", "PENDING")

            return Ok(f"Due date changed to [b cyan]{self.value}[/b cyan]")

        return Warn("Cannot parse the string!")

    def to_txt(self) -> str:
        return f"due:{self.value}"

    def from_txt(self, txt: str) -> None:
        self.set(txt.split()[2].lstrip("due:"))


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
        self.value = txt.split()[1][1]


class Tags(Item):
    value = ""

    def set(self, val: str) -> Result:
        tags = [i.strip() for i in val.split(",") if i]
        self.value = ",".join(set(tags))
        return Ok()

    def add_tag(self, tag: str):
        return self.set(self.value + "," + tag)

    def to_txt(self):
        return " ".join(f"@{i}" for i in self.value.split(","))

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
        res = split_duration(val.strip())
        if not res:
            return Warn("Invalid Format! Use: <number><m/h/d/w>")

        if not val:
            self.value = ""
            return Ok("Recurrence removed")

        self.value = val
        if self.model.due == "none":
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


class Effort(Item):
    pass
