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
        self.topic = self.children.pop()

    def commit(self):
        """
        Create obj data to be saved
        """

        d = {getattr(child, "about"): child.commit() for child in self.children}
        return {"common": self.topic.commit(), **d}

    def from_data(self, data):
        """
        Setup object from stored data
        """

        for i, j in data.items():
            if i == "common":
                self.topic.edit("about", i)
                self.topic.from_data(j)
            else:
                self.add_child()
                self.children[-1].edit("about", i)
                self.children[-1].from_data(j)
