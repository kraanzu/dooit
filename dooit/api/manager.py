from .model import Model
from typing import Optional, Type
from ..utils import Parser

class Manager(Model):
    fields = []
    nomenclature: str = "Workspace"

    def __init__(self, name: str, parent: Optional["Model"] = None) -> None:
        from .workspace import Workspace

        super().__init__(name, parent)
        self.ctype: Type = Workspace

    def commit(self):
        data = super().commit()
        Parser.save(data)

    def setup(self):
        data = Parser.load()
        self.from_data(data)


manager = Manager(name="Manager")
manager.setup()
