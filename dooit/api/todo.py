from typing import Optional
from .model import Model


class Todo(Model):
    fields = ["about", "due", "urgency"]
    nomenclature: str = "Todo"

    def __init__(self, name: str, parent: Optional["Model"] = None) -> None:
        super().__init__(name, parent)

        self.about = ""
        self.due = "today"
        self.urgency = 4
        self.status = "PENDING"
        self.ctype = type(self)

        self.opts = {
            "PENDING": "x",
            "COMPLETED": "X",
            "OVERDUE": "O",
        }

    def to_data(self) -> str:

        # status = self.opts[self.status]
        return f"{self.status} ({self.urgency}) due:{self.due or 'None'} {self.about}"

    def fill_from_data(self, data: str):
        status, urgency, due, *about = data.split()

        # status = self.opts[status]
        about = " ".join(about)

        due = due[4:]
        if due == "None":
            due = ""

        urgency = int(urgency[1:-1])

        self.about = about
        self.urgency = urgency
        self.due = due
        self.status = status

    def commit(self):
        if self.children:
            return [self.to_data(), [child.commit() for child in self.children]]
        else:
            return [self.to_data()]

    def from_data(self, data):
        for i in data:
            self.add_child()
            self.children[-1].fill_from_data(i[0])
            if len(i) > 1:
                self.children[-1].from_data(i[1])

    def get_todos(self):
        return self.children
