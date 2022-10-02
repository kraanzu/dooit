from typing import Callable, Optional
from model import Model


class Todo(Model):
    fields = ["about", "due", "urgency"]
    nomenclature: str = "Todo"

    def __init__(self, name: str, parent: Optional["Model"] = None) -> None:
        super().__init__(name, parent)

        self.about = name
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
        self.date = due
        self.status = status

    def export(self):
        return [self.to_data(), [child.export() for child in self.children]]

    def from_file(self, data):
        for i, j in data:
            self.add_child()
            self.children[-1].fill_from_data(i)
            self.children[-1].from_export(j)


class Topic(Model):
    fields = ["about"]
    nomenclature: str = "Todo"

    def __init__(self, name: str, parent: Optional["Model"] = None) -> None:
        super().__init__(name, parent)
        self.about = name
        self.ctype: Callable = Todo

    def export(self):
        return [child.export() for child in self.children]

    def from_file(self, data):
        for i, j in data:
            self.add_child()
            self.children[-1].fill_from_data(i)
            self.children[-1].from_export(j)


class Workspace(Model):
    fields = ["about"]
    nomenclature: str = "Topic"

    def __init__(self, name: str, parent: Optional["Model"] = None) -> None:
        super().__init__(name, parent)
        self._about = name
        self.ctype: Callable = Topic


class Manager(Model):
    fields = []
    nomenclature: str = "Workspace"

    def __init__(self, name: str, parent: Optional["Model"] = None) -> None:
        super().__init__(name, parent)
        self.ctype: Callable = Workspace


manager = Manager(name="Manager")
for i in range(5):
    manager.add_child()
    manager.children[-1].add_child()
    manager.children[-1].children[-1].add_child()
