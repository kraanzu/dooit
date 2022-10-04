from typing import Optional, Callable
from .model import Model


class Workspace(Model):
    fields = ["about"]
    nomenclature: str = "Topic"

    def __init__(self, name: str, parent: Optional["Model"] = None) -> None:
        from .topic import Topic

        super().__init__(name, parent)
        self.about = ""
        self.ctype: Callable = Topic
        self.add_child()
