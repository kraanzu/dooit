from typing import Callable, Optional
from model import Model


class Todo(Model):
    fields = ["about", "date", "urgency"]
    nomenclature: str = "Todo"

    def __init__(self, name: str, parent: Optional["Model"] = None) -> None:
        super().__init__(name, parent)
        self.about = name
        self.date = "today"
        self.urgency = 4
        self.ctype = type(self)

    def get_export(self):
        return [self.about, [child.get_export() for child in self.children]]


class Topic(Model):
    fields = ["about"]
    nomenclature: str = "Todo"

    def __init__(self, name: str, parent: Optional["Model"] = None) -> None:
        super().__init__(name, parent)
        self.about = name
        self.ctype: Callable = Todo

    def get_export(self):
        return [child.get_export() for child in self.children]


class Workspace(Model):
    fields = ["about"]
    nomenclature: str = "Topic"

    def __init__(self, name: str, parent: Optional["Model"] = None) -> None:
        super().__init__(name, parent)
        self.about = name
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
